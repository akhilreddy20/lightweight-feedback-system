from fastapi import APIRouter, HTTPException
from models import UserCreate, UserLogin
from database import users_collection
from utils import hash_password, verify_password, create_token

auth_router = APIRouter()

@auth_router.post("/register")
async def register_user(user: UserCreate):
    print("Incoming registration:", user.dict())

    # ✅ Step 2: MongoDB sanity check
    try:
        ping_result = await users_collection.database.command("ping")
        print("✅ MongoDB Ping Successful:", ping_result)
    except Exception as ping_error:
        print("❌ MongoDB Ping Failed:", ping_error)
        raise HTTPException(status_code=500, detail="MongoDB is not reachable")

    try:
        existing_user = await users_collection.find_one({"username": user.username})
        print("Existing user check:", existing_user)

        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_pw = hash_password(user.password)
        print("Hashed password created")

        user_dict = user.dict()
        user_dict["password"] = hashed_pw

        result = await users_collection.insert_one(user_dict)
        print("Inserted user with ID:", str(result.inserted_id))

        return {"msg": "User created successfully"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.post("/login")
async def login(user: UserLogin):
    try:
        db_user = await users_collection.find_one({"username": user.username})
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_token({"username": user.username, "role": db_user["role"]})
        return {"token": token, "role": db_user["role"]}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Login failed due to server error")
