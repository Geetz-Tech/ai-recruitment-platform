from sqlalchemy.orm import Session
from ..core.security import get_password_hash
from .models import User
from .schemas import UserCreate


class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=get_password_hash(user.password),
            role=user.role,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()
