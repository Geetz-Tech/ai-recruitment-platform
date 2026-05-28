from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, require_role
from ..users.models import User
from .service import ApplicationService
from .schemas import ApplicationCreate, ApplicationStageUpdate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: Session = Depends(get_db),
):
    db_app = ApplicationService.create_application(db, application)
    return db_app


@router.get("", response_model=list[ApplicationResponse])
async def get_applications(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    applications = ApplicationService.get_all_applications(db, skip=skip, limit=limit)
    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = ApplicationService.get_application_by_id(db, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    return application


@router.patch("/{application_id}/stage", response_model=ApplicationResponse)
async def update_application_stage(
    application_id: int,
    stage_update: ApplicationStageUpdate,
    current_user: User = Depends(require_role("admin", "recruiter", "hiring_manager")),
    db: Session = Depends(get_db),
):
    application = ApplicationService.update_application_stage(db, application_id, stage_update)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    return application
