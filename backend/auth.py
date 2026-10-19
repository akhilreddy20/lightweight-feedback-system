import logging

from fastapi import APIRouter, Header, HTTPException
from jose import JWTError

from database import users_collection
from models import UserCreate, UserLogin
from utils import create_token, decode_token, hash_password, verify_password

logger = logging.getLogger("feedback.auth")
auth_router = APIRouter()


@auth_router.post("/register", status_code=201)
async def register_user(user: UserCreate):
    # HTTPExceptions propagate as-is. Previously a broad `except Exception`
    # turned "Username already exists" (400) into a 500.
    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)
    await users_collection.insert_one(user_dict)
    # Never log request bodies: they contain passwords.
    logger.info("user registered", extra={"username": user.username, "role": user.role})
    return {"msg": "User created successfully"}


@auth_router.post("/login")
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        # Previously caught by `except Exception` and returned as 500.
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"username": db_user["username"], "role": db_user["role"]})
    return {"token": token, "role": db_user["role"]}


async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        payload = decode_token(authorization.removeprefix("Bearer ").strip())
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username, role = payload.get("username"), payload.get("role")
    if not username or not role:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {"username": username, "role": role}
