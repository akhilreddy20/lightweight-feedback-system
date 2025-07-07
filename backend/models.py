from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'manager' or 'employee'

class UserLogin(BaseModel):
    username: str
    password: str


class FeedbackCreate(BaseModel):
    strengths: str
    areas_to_improve: str
    sentiment: str  # positive / neutral / negative

class FeedbackInDB(FeedbackCreate):
    manager_username: str
    employee_id: str


class TokenData(BaseModel):
    username: str
    role: str