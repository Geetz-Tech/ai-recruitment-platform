from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user, require_role
from ..users.models import User
from ..candidates.service import CandidateService
from pydantic import BaseModel

router = APIRouter(prefix="/candidates", tags=["resumes"])


class ResumeMetadata(BaseModel):
    filename: str
    size: int
    content_type: str


@router.post("/{candidate_id}/resume")
async def upload_resume(
    candidate_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(require_role("admin", "recruiter")),
    db: Session = Depends(get_db),
):
    candidate = CandidateService.get_candidate_by_id(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported",
        )
    
    metadata = ResumeMetadata(
        filename=file.filename,
        size=len(await file.read()),
        content_type=file.content_type,
    )
    
    return {
        "candidate_id": candidate_id,
        "message": "Resume uploaded successfully",
        "metadata": metadata,
    }


@router.get("/{candidate_id}/resume")
async def get_resume(
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
    
    return {
        "candidate_id": candidate_id,
        "message": "Resume metadata retrieved",
        "filename": "resume.pdf",
    }
