from pydantic import BaseModel
from datetime import datetime


class JobOpeningBase(BaseModel):
    title: str
    description: str
    department: str | None = None
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    recruiter_id: int | None = None
    hiring_manager_id: int | None = None


class JobOpeningCreate(JobOpeningBase):
    pass


class JobOpeningUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    department: str | None = None
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    recruiter_id: int | None = None
    hiring_manager_id: int | None = None
    is_open: bool | None = None


class JobOpeningResponse(JobOpeningBase):
    id: int
    is_open: bool
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
