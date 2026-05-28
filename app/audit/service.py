from sqlalchemy.orm import Session
from .models import ActivityLog, CandidateNote


class AuditService:
    @staticmethod
    def log_activity(
        db: Session,
        user_id: int,
        action: str,
        resource_type: str,
        resource_id: int,
        description: str | None = None,
    ) -> ActivityLog:
        log = ActivityLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def add_candidate_note(
        db: Session, candidate_id: int, user_id: int, note_text: str
    ) -> CandidateNote:
        note = CandidateNote(
            candidate_id=candidate_id, user_id=user_id, note_text=note_text
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def get_candidate_notes(db: Session, candidate_id: int):
        return db.query(CandidateNote).filter(CandidateNote.candidate_id == candidate_id).all()

    @staticmethod
    def get_activity_logs(db: Session, user_id: int | None = None, limit: int = 100):
        query = db.query(ActivityLog)
        if user_id:
            query = query.filter(ActivityLog.user_id == user_id)
        return query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
