from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user
from database import feedbacks_collection, users_collection
from models import FeedbackCreate, FeedbackInDB, FeedbackUpdate


router = APIRouter(prefix="/feedback")


@router.get("/team")
async def get_team(user=Depends(get_current_user)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can access this")

    employees = await users_collection.find({"role": "employee"}).to_list(100)
    return [
        {"_id": str(emp["_id"]), "username": emp["username"]}
        for emp in employees
    ]


# Submit feedback (Manager only)
@router.post("/{employee_id}")
async def add_feedback(employee_id: str, fb: FeedbackCreate, user=Depends(get_current_user)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can submit feedback")

    try:
        obj_id = ObjectId(employee_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid employee ID format")

    employee = await users_collection.find_one({"_id": obj_id, "role": "employee"})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    doc = FeedbackInDB(
        **fb.model_dump(),
        manager_username=user["username"],
        employee_id=employee_id,
    ).model_dump()
    # Lists are sorted by timestamp, which was previously never set.
    doc["timestamp"] = datetime.now(timezone.utc)
    doc["acknowledged"] = False
    result = await feedbacks_collection.insert_one(doc)
    return {"status": "ok", "id": str(result.inserted_id)}


# Get feedback history (visible to employee or their manager)
@router.get("/{employee_id}")
async def feedback_history(employee_id: str, user=Depends(get_current_user)):
    try:
        obj_id = ObjectId(employee_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid employee ID format")

    employee = await users_collection.find_one({"_id": obj_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if user["role"] == "employee" and user["username"] != employee["username"]:
        raise HTTPException(status_code=403, detail="Access denied")

    feedbacks = await feedbacks_collection.find({"employee_id": employee_id}).sort("timestamp", -1).to_list(100)
    for fb in feedbacks:
        fb["_id"] = str(fb["_id"])
        if "timestamp" in fb:
            fb["timestamp"] = fb["timestamp"].isoformat()

    return feedbacks

@router.get("/", summary="Employee fetch own feedback")
async def get_my_feedback(user=Depends(get_current_user)):
    if user["role"] != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    employee = await users_collection.find_one({"username": user["username"]})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee_id = str(employee["_id"])

    feedbacks = await feedbacks_collection.find(
        {"employee_id": employee_id}
    ).sort("timestamp", -1).to_list(100)

    for fb in feedbacks:
        fb["_id"] = str(fb["_id"])
        if "timestamp" in fb:
            fb["timestamp"] = fb["timestamp"].isoformat()

    return feedbacks



@router.patch("/{feedback_id}/acknowledge")
async def acknowledge_feedback(feedback_id: str, user=Depends(get_current_user)):
    if user["role"] != "employee":
        raise HTTPException(status_code=403, detail="Only employees can acknowledge feedback")

    try:
        obj_id = ObjectId(feedback_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid feedback ID")

    employee = await users_collection.find_one({"username": user["username"]})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Scope to the caller: previously any employee could acknowledge anyone's feedback.
    result = await feedbacks_collection.update_one(
        {"_id": obj_id, "employee_id": str(employee["_id"])},
        {"$set": {"acknowledged": True, "acknowledged_at": datetime.now(timezone.utc)}},
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Feedback not found or already acknowledged")

    return {"status": "acknowledged"}


@router.patch("/{feedback_id}/edit")
async def edit_feedback(feedback_id: str, data: FeedbackUpdate, user=Depends(get_current_user)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can edit feedback")

    try:
        obj_id = ObjectId(feedback_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid feedback ID")

    result = await feedbacks_collection.update_one(
        {"_id": obj_id, "manager_username": user["username"]},
        {"$set": {**data.model_dump(), "updated_at": datetime.now(timezone.utc)}},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Feedback not found or not owned by you")

    return {"status": "updated"}
