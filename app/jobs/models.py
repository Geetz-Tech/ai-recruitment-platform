from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..core.database import Base


class JobOpening(Base):
    __tablename__ = "job_openings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    department = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hiring_manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_open = Column(String, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
