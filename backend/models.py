from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'manager' or 'employee'

class UserLogin(BaseModel):
    username: str
    password: str
