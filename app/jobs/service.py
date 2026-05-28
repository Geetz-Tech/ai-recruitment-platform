from sqlalchemy.orm import Session
from .models import JobOpening
from .schemas import JobOpeningCreate, JobOpeningUpdate


class JobService:
    @staticmethod
    def create_job(db: Session, job: JobOpeningCreate) -> JobOpening:
        db_job = JobOpening(**job.model_dump())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job

    @staticmethod
    def get_job_by_id(db: Session, job_id: int) -> JobOpening | None:
        return db.query(JobOpening).filter(JobOpening.id == job_id).first()

    @staticmethod
    def get_all_jobs(db: Session, skip: int = 0, limit: int = 100):
        return db.query(JobOpening).offset(skip).limit(limit).all()

    @staticmethod
    def update_job(db: Session, job_id: int, job: JobOpeningUpdate) -> JobOpening | None:
        db_job = JobService.get_job_by_id(db, job_id)
        if not db_job:
            return None
        
        update_data = job.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_job, field, value)
        
        db.commit()
        db.refresh(db_job)
        return db_job

    @staticmethod
    def delete_job(db: Session, job_id: int) -> bool:
        db_job = JobService.get_job_by_id(db, job_id)
        if not db_job:
            return False
        
        db.delete(db_job)
        db.commit()
        return True
