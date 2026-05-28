from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Literal["admin", "recruiter", "hiring_manager"] = "recruiter"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: Literal["admin", "recruiter", "hiring_manager"] | None = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    pass
