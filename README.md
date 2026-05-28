# AI-Assisted Recruitment Workflow Platform

A modern backend system for managing recruitment workflows, candidate tracking, and job openings. This project demonstrates clean architecture, authentication, role-based access control (RBAC), and AI-assisted candidate summary generation.

## Overview

This platform is designed to streamline recruitment processes with:

- **User Management**: Multi-role authentication system (Admin, Recruiter, Hiring Manager)
- **Candidate Tracking**: Manage candidate profiles and track application progression
- **Job Openings**: Create and manage job requisitions with team assignments
- **Workflow Automation**: Track candidates through recruitment stages (applied → hired/rejected)
- **AI Integration**: Generate candidate summaries using mock or OpenAI providers
- **Activity Auditing**: Complete audit logs and candidate notes for transparency

## Purpose

This is a portfolio-safe demonstration project created to showcase:

- Backend architecture patterns for SaaS applications
- Authentication and authorization implementation
- RESTful API design with FastAPI
- Database modeling and migrations with SQLAlchemy/Alembic
- Recruitment workflow domain design
- Docker containerization for deployment
- Clean code principles and professional structure

This project does not contain private company code, client data, or production business logic.

## Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Authentication**: JWT with bcrypt password hashing
- **API Documentation**: Swagger/OpenAPI (auto-generated)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest

## Features

### Authentication & Authorization

- User registration and login
- JWT token-based authentication
- Role-based access control (3 roles: admin, recruiter, hiring_manager)
- Secure password hashing with bcrypt

### Candidate Management

- Create and update candidate profiles
- Track candidates through recruitment stages
- Store contact information and source tracking
- Candidate status workflow (applied → screening → interview → offer → hired/rejected)

### Job Management

- Create and publish job openings
- Assign recruiters and hiring managers
- Track salary ranges and department information
- Job status management

### Application Tracking

- Submit candidate applications to job openings
- Update application stages through workflow
- Track application history and timelines

### AI-Assisted Features

- Generate candidate summaries using mock service (default) or OpenAI API
- Extensible provider architecture for multiple AI backends

### Dashboard & Analytics

- Summary metrics (total candidates, open jobs)
- Candidates grouped by stage
- Application metrics and tracking

### Audit & Notes

- Complete activity logs for compliance
- Recruiter notes on candidates
- Timestamp tracking for all changes

## API Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login and receive JWT token
- GET /auth/me - Get current user info

### Users
- GET /users - List all users (admin only)
- GET /users/{id} - Get user details (admin only)

### Candidates
- POST /candidates - Create candidate
- GET /candidates - List candidates
- GET /candidates/{id} - Get candidate details
- PUT /candidates/{id} - Update candidate
- DELETE /candidates/{id} - Delete candidate

### Jobs
- POST /jobs - Create job opening
- GET /jobs - List job openings
- GET /jobs/{id} - Get job details
- PUT /jobs/{id} - Update job opening
- DELETE /jobs/{id} - Delete job opening

### Applications
- POST /applications - Create application
- GET /applications - List applications
- GET /applications/{id} - Get application details
- PATCH /applications/{id}/stage - Update application stage

### Resume Handling
- POST /candidates/{id}/resume - Upload resume
- GET /candidates/{id}/resume - Get resume metadata

### Dashboard
- GET /dashboard/summary - Get dashboard metrics
- GET /dashboard/candidates-by-stage - Candidates grouped by stage
- GET /dashboard/applications - Application metrics

## Database Schema

Core entities include: User (authentication), Candidate (profiles), JobOpening (requisitions), Application (tracking), ActivityLog (audit), and CandidateNote (feedback).

## Project Structure

```
ai-recruitment-platform/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── auth/
│   ├── users/
│   ├── candidates/
│   ├── jobs/
│   ├── applications/
│   ├── resumes/
│   ├── ai/
│   ├── dashboard/
│   └── audit/
├── tests/
├── alembic/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### With Docker (Recommended)

```bash
git clone <repository-url>
cd ai-recruitment-platform
docker-compose up
```

API available at http://localhost:8000

### Without Docker

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Configure DATABASE_URL in .env
alembic upgrade head
python scripts_seed.py
uvicorn app.main:app --reload
```

## Demo Credentials

After seeding:
- Admin: admin@example.com / admin123
- Recruiter: recruiter@example.com / recruiter123
- Manager: manager@example.com / manager123

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

## Architecture Highlights

- Clean separation of concerns (routers, services, models, schemas)
- Dependency injection for database and authentication
- Full type hints for clarity
- JWT-based authentication with bcrypt hashing
- RBAC for fine-grained access control
- SQLAlchemy ORM with Alembic migrations
- RESTful API design with Pydantic schemas
- Docker containerization for reproducible deployment

## License

Portfolio demonstration project.

---

Portfolio Disclaimer: This project was created as a portfolio-safe demonstration of backend architecture, recruitment workflow design, API development, authentication, RBAC, and AI-assisted workflow patterns. It does not contain private company code, client data, or production business logic.
