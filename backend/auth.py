from fastapi import APIRouter, HTTPException, Depends, Request, Header
from fastapi.security import OAuth2PasswordBearer
from models import UserCreate, UserLogin, TokenData
from database import users_collection
from utils import hash_password, verify_password, create_token
from jose import jwt, JWTError

auth_router = APIRouter()

# 🔐 Use a dummy tokenUrl because we handle login ourselves
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")






@auth_router.post("/register")
async def register_user(user: UserCreate):
    print("Incoming registration:", user.dict())

    try:
        ping_result = await users_collection.database.command("ping")
        print("✅ MongoDB Ping Successful:", ping_result)
    except Exception as ping_error:
        print("❌ MongoDB Ping Failed:", ping_error)
        raise HTTPException(status_code=500, detail="MongoDB is not reachable")

    try:
        # ✅ Check for existing user
        existing_user = await users_collection.find_one({"username": user.username})
        print("Existing user check:", existing_user)

        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # ✅ Hash password
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


# ✅ Used in protected routes to extract the user from JWT token
async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        role = payload.get("role")
        if not username or not role:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"username": username, "role": role}
    except JWTError as e:
        print("❌ Token Decode Error:", e)
        raise HTTPException(status_code=401, detail="Token decode failed")
