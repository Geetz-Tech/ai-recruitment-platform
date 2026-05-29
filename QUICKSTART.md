# Getting Started

## Docker Setup (Recommended)

### 30-Second Setup
`ash
docker-compose up
`

API available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Development Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Recruiter | recruiter@example.com | recruiter123 |
| Hiring Manager | manager@example.com | manager123 |

### First API Call

1. Navigate to http://localhost:8000/docs
2. Click "Authorize" button
3. Use POST /auth/login with development credentials above
4. Copy the ccess_token from the response
5. Click "Authorize" again and paste: Bearer <token>
6. Try any endpoint (e.g., GET /candidates)

## Local Installation

`ash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your database URL

# Run migrations
alembic upgrade head

# Seed initial data
python scripts_seed.py

# Start server
uvicorn app.main:app --reload
`

API available at http://localhost:8000/docs

## Useful Commands

### Docker
`ash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f api

# Access database directly
docker-compose exec db psql -U recruitment_user recruitment_db
`

### Testing
`ash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_auth.py -v
`

### Database
`ash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
`

## Environment Configuration

Edit .env to customize:

`
# Database
DATABASE_URL=postgresql://user:password@localhost/recruitment_db

# Security
SECRET_KEY=<your-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI/Insights Provider
INSIGHTS_PROVIDER=openai           # or: mock (default)
OPENAI_API_KEY=<your-api-key>     # Required if using OpenAI
OPENAI_MODEL=gpt-3.5-turbo

# Debug
DEBUG=False
`

See .env.example for all available options.

## Project Layout

- **app/auth** - Authentication and user registration
- **app/users** - User management
- **app/candidates** - Candidate profiles and tracking
- **app/jobs** - Job opening management
- **app/applications** - Application workflow tracking
- **app/resumes** - Resume upload handling
- **app/ai** - Candidate insights engine
- **app/dashboard** - Analytics and reporting
- **app/audit** - Activity logging and notes
- **tests/** - Test suite

## Next Steps

1. Review [README.md](README.md) for complete documentation
2. Explore [ARCHITECTURE.md](ARCHITECTURE.md) for design details
3. Check the API docs at http://localhost:8000/docs
4. Run the test suite with pytest tests/ -v

---

For production deployment, see README.md section on Deployment.
