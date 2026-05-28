from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, require_role
from ..users.models import User
from .models import Candidate
from .service import CandidateService
from .schemas import CandidateCreate, CandidateUpdate, CandidateResponse

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("", response_model=CandidateResponse)
async def create_candidate(
    candidate: CandidateCreate,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: Session = Depends(get_db),
):
    existing = CandidateService.get_candidate_by_email(db, candidate.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate with this email already exists",
        )
    
    db_candidate = CandidateService.create_candidate(db, candidate)
    return db_candidate


@router.get("", response_model=list[CandidateResponse])
async def get_candidates(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    candidates = CandidateService.get_all_candidates(db, skip=skip, limit=limit, status=status)
    return candidates


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    candidate = CandidateService.get_candidate_by_id(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: int,
    candidate_update: CandidateUpdate,
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: Session = Depends(get_db),
):
    candidate = CandidateService.update_candidate(db, candidate_id, candidate_update)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    if not CandidateService.delete_candidate(db, candidate_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
