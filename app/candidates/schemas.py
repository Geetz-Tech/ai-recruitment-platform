from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal


class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    source: str | None = None
    linkedin_url: str | None = None


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    source: str | None = None
    linkedin_url: str | None = None


class CandidateResponse(CandidateBase):
    id: int
    current_status: Literal["applied", "screening", "shortlisted", "interview", "offer", "rejected", "hired"]
    summary: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
