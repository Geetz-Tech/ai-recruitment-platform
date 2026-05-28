from sqlalchemy.orm import Session
from ..core.security import verify_password, create_access_token
from ..users.service import UserService
from ..users.models import User


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User | None:
        user = UserService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token_for_user(user: User) -> str:
        return create_access_token(data={"sub": str(user.id)})
