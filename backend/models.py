from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["manager", "employee"]
Sentiment = Literal["positive", "neutral", "negative"]


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=72)  # bcrypt limit
    role: Role


class UserLogin(BaseModel):
    username: str
    password: str


class FeedbackCreate(BaseModel):
    strengths: str = Field(min_length=1, max_length=2000)
    areas_to_improve: str = Field(min_length=1, max_length=2000)
    sentiment: Sentiment


class FeedbackUpdate(FeedbackCreate):
    pass


class FeedbackInDB(FeedbackCreate):
    manager_username: str
    employee_id: str
