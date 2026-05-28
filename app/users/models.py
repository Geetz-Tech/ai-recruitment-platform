from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    recruiter = "recruiter"
    hiring_manager = "hiring_manager"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.recruiter, nullable=False)
    is_active = Column(String, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
