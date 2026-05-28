from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class CandidateStatus(str, enum.Enum):
    applied = "applied"
    screening = "screening"
    shortlisted = "shortlisted"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    hired = "hired"


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    current_status = Column(Enum(CandidateStatus), default=CandidateStatus.applied)
    summary = Column(Text, nullable=True)
    source = Column(String(100), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
