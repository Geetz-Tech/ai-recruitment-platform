from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, require_role
from ..users.models import User
from .service import UserService
from .schemas import UserResponse, UserDetailResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    users = UserService.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=UserDetailResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
