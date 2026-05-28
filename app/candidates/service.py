from sqlalchemy.orm import Session
from .models import Candidate, CandidateStatus
from .schemas import CandidateCreate, CandidateUpdate


class CandidateService:
    @staticmethod
    def create_candidate(db: Session, candidate: CandidateCreate) -> Candidate:
        db_candidate = Candidate(**candidate.model_dump())
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        return db_candidate

    @staticmethod
    def get_candidate_by_id(db: Session, candidate_id: int) -> Candidate | None:
        return db.query(Candidate).filter(Candidate.id == candidate_id).first()

    @staticmethod
    def get_candidate_by_email(db: Session, email: str) -> Candidate | None:
        return db.query(Candidate).filter(Candidate.email == email).first()

    @staticmethod
    def get_all_candidates(
        db: Session, skip: int = 0, limit: int = 100, status: str | None = None
    ):
        query = db.query(Candidate)
        if status:
            query = query.filter(Candidate.current_status == status)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_candidate(db: Session, candidate_id: int, candidate: CandidateUpdate) -> Candidate | None:
        db_candidate = CandidateService.get_candidate_by_id(db, candidate_id)
        if not db_candidate:
            return None
        
        update_data = candidate.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_candidate, field, value)
        
        db.commit()
        db.refresh(db_candidate)
        return db_candidate

    @staticmethod
    def update_candidate_status(db: Session, candidate_id: int, status: str) -> Candidate | None:
        db_candidate = CandidateService.get_candidate_by_id(db, candidate_id)
        if not db_candidate:
            return None
        
        db_candidate.current_status = status
        db.commit()
        db.refresh(db_candidate)
        return db_candidate

    @staticmethod
    def delete_candidate(db: Session, candidate_id: int) -> bool:
        db_candidate = CandidateService.get_candidate_by_id(db, candidate_id)
        if not db_candidate:
            return False
        
        db.delete(db_candidate)
        db.commit()
        return True
