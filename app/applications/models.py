from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Enum
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class ApplicationStage(str, enum.Enum):
    applied = "applied"
    screening = "screening"
    shortlisted = "shortlisted"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    hired = "hired"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_openings.id"), nullable=False)
    stage = Column(Enum(ApplicationStage), default=ApplicationStage.applied)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
