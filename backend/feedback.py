from fastapi import APIRouter, Depends, HTTPException
from database import feedbacks_collection, users_collection
from models import FeedbackCreate, FeedbackInDB
from auth import get_current_user
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Body


router = APIRouter(prefix="/feedback")


# ✅ Add this new route
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
        **fb.dict(),
        manager_username=user["username"],
        employee_id=employee_id
    )
    await feedbacks_collection.insert_one(doc.dict())
    return {"status": "ok"}


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

    # 🔍 Get this employee's ID from the users_collection
    employee = await users_collection.find_one({"username": user["username"]})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee_id = str(employee["_id"])

    # ✅ Fetch feedbacks by employee_id
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

    result = await feedbacks_collection.update_one(
        {"_id": obj_id},
        {"$set": {"acknowledged": True}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Feedback not found or already acknowledged")

    return {"status": "acknowledged"}


@router.patch("/{feedback_id}/edit")
async def edit_feedback(feedback_id: str, data: dict = Body(...), user=Depends(get_current_user)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Only managers can edit feedback")

    try:
        obj_id = ObjectId(feedback_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid feedback ID")

    result = await feedbacks_collection.update_one(
        {"_id": obj_id, "manager_username": user["username"]},
        {"$set": {
            "strengths": data.get("strengths"),
            "areas_to_improve": data.get("areas_to_improve"),
            "sentiment": data.get("sentiment"),
        }}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Feedback not found or not owned by you")

    return {"status": "updated"}
