import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.users.models import User, UserRole
from app.candidates.models import Candidate
from app.jobs.models import JobOpening


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created")


def seed_data():
    db = SessionLocal()
    
    try:
        admin_user = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.admin,
            is_active=True,
        )
        
        recruiter_user = User(
            email="recruiter@example.com",
            full_name="Recruiter User",
            hashed_password=get_password_hash("recruiter123"),
            role=UserRole.recruiter,
            is_active=True,
        )
        
        hiring_manager_user = User(
            email="manager@example.com",
            full_name="Hiring Manager",
            hashed_password=get_password_hash("manager123"),
            role=UserRole.hiring_manager,
            is_active=True,
        )
        
        db.add(admin_user)
        db.add(recruiter_user)
        db.add(hiring_manager_user)
        db.flush()
        
        candidate1 = Candidate(
            first_name="Alice",
            last_name="Johnson",
            email="alice@example.com",
            phone="555-0001",
            source="LinkedIn",
        )
        
        candidate2 = Candidate(
            first_name="Bob",
            last_name="Smith",
            email="bob@example.com",
            phone="555-0002",
            source="Referral",
        )
        
        db.add(candidate1)
        db.add(candidate2)
        db.flush()
        
        job1 = JobOpening(
            title="Senior Backend Engineer",
            description="Looking for an experienced backend engineer with Python expertise",
            department="Engineering",
            location="Remote",
            salary_min=120000,
            salary_max=160000,
            recruiter_id=recruiter_user.id,
            hiring_manager_id=hiring_manager_user.id,
            is_open=True,
        )
        
        job2 = JobOpening(
            title="Product Manager",
            description="Seeking a PM to lead our product strategy",
            department="Product",
            location="San Francisco",
            salary_min=150000,
            salary_max=200000,
            recruiter_id=recruiter_user.id,
            is_open=True,
        )
        
        db.add(job1)
        db.add(job2)
        db.commit()
        
        print("Seed data created successfully")
        print(f"Admin user: admin@example.com / admin123")
        print(f"Recruiter user: recruiter@example.com / recruiter123")
        print(f"Manager user: manager@example.com / manager123")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    seed_data()
