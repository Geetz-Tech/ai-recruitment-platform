from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..users.models import User
from ..users.schemas import UserResponse
from ..users.service import UserService
from .schemas import RegisterRequest, LoginRequest, TokenResponse
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = UserService.get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = UserService.create_user(
        db,
        UserCreate(
            email=request.email,
            full_name=request.full_name,
            password=request.password,
        ),
    )
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user = AuthService.authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    access_token = AuthService.create_access_token_for_user(user)
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    return current_user


# Import here to avoid circular dependency
from ..users.schemas import UserCreate
