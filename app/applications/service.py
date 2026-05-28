from sqlalchemy.orm import Session
from .models import Application
from .schemas import ApplicationCreate, ApplicationStageUpdate


class ApplicationService:
    @staticmethod
    def create_application(db: Session, application: ApplicationCreate) -> Application:
        db_app = Application(**application.model_dump())
        db.add(db_app)
        db.commit()
        db.refresh(db_app)
        return db_app

    @staticmethod
    def get_application_by_id(db: Session, application_id: int) -> Application | None:
        return db.query(Application).filter(Application.id == application_id).first()

    @staticmethod
    def get_all_applications(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Application).offset(skip).limit(limit).all()

    @staticmethod
    def get_applications_by_candidate(db: Session, candidate_id: int):
        return db.query(Application).filter(Application.candidate_id == candidate_id).all()

    @staticmethod
    def update_application_stage(db: Session, application_id: int, update: ApplicationStageUpdate) -> Application | None:
        db_app = ApplicationService.get_application_by_id(db, application_id)
        if not db_app:
            return None
        
        db_app.stage = update.stage
        db.commit()
        db.refresh(db_app)
        return db_app

    @staticmethod
    def delete_application(db: Session, application_id: int) -> bool:
        db_app = ApplicationService.get_application_by_id(db, application_id)
        if not db_app:
            return False
        
        db.delete(db_app)
        db.commit()
        return True
