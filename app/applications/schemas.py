from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class ApplicationBase(BaseModel):
    candidate_id: int
    job_id: int


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationStageUpdate(BaseModel):
    stage: Literal["applied", "screening", "shortlisted", "interview", "offer", "rejected", "hired"]


class ApplicationResponse(ApplicationBase):
    id: int
    stage: Literal["applied", "screening", "shortlisted", "interview", "offer", "rejected", "hired"]
    applied_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
