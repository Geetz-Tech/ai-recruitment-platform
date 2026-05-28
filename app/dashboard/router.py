from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..users.models import User
from .service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardService.get_summary(db)


@router.get("/candidates-by-stage")
async def get_candidates_by_stage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardService.get_candidates_by_stage(db)


@router.get("/applications")
async def get_application_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardService.get_application_metrics(db)
