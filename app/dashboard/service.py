from sqlalchemy.orm import Session
from sqlalchemy import func
from ..candidates.models import Candidate
from ..jobs.models import JobOpening
from ..applications.models import Application


class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> dict:
        total_candidates = db.query(func.count(Candidate.id)).scalar() or 0
        open_jobs = db.query(func.count(JobOpening.id)).filter(JobOpening.is_open == True).scalar() or 0
        
        return {
            "total_candidates": total_candidates,
            "open_jobs": open_jobs,
        }

    @staticmethod
    def get_candidates_by_stage(db: Session) -> dict:
        stages = db.query(
            Candidate.current_status,
            func.count(Candidate.id).label("count")
        ).group_by(Candidate.current_status).all()
        
        return {stage: count for stage, count in stages}

    @staticmethod
    def get_application_metrics(db: Session) -> dict:
        total_applications = db.query(func.count(Application.id)).scalar() or 0
        by_stage = db.query(
            Application.stage,
            func.count(Application.id).label("count")
        ).group_by(Application.stage).all()
        
        return {
            "total_applications": total_applications,
            "by_stage": {stage: count for stage, count in by_stage},
        }
