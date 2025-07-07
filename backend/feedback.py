from fastapi import APIRouter, Depends, HTTPException
from database import feedbacks_collection, users_collection
from models import FeedbackCreate, FeedbackInDB
from auth import get_current_user
from bson import ObjectId
from bson.errors import InvalidId

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

    feedbacks = await feedbacks_collection.find({"employee_id": {"$exists": True}, "employee_username": user["username"]}).sort("timestamp", -1).to_list(100)

    for fb in feedbacks:
        fb["_id"] = str(fb["_id"])
        if "timestamp" in fb:
            fb["timestamp"] = fb["timestamp"].isoformat()

    return feedbacks
