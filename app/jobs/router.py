from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, require_role
from ..users.models import User
from .service import JobService
from .schemas import JobOpeningCreate, JobOpeningUpdate, JobOpeningResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobOpeningResponse)
async def create_job(
    job: JobOpeningCreate,
    current_user: User = Depends(require_role("admin", "hiring_manager")),
    db: Session = Depends(get_db),
):
    db_job = JobService.create_job(db, job)
    return db_job


@router.get("", response_model=list[JobOpeningResponse])
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jobs = JobService.get_all_jobs(db, skip=skip, limit=limit)
    return jobs


@router.get("/{job_id}", response_model=JobOpeningResponse)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = JobService.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job opening not found",
        )
    return job


@router.put("/{job_id}", response_model=JobOpeningResponse)
async def update_job(
    job_id: int,
    job_update: JobOpeningUpdate,
    current_user: User = Depends(require_role("admin", "hiring_manager")),
    db: Session = Depends(get_db),
):
    job = JobService.update_job(db, job_id, job_update)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job opening not found",
        )
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    if not JobService.delete_job(db, job_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job opening not found",
        )
