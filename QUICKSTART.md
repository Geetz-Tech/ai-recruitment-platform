# Quick Start Guide

## 30-Second Setup with Docker

```bash
docker-compose up
```

Then visit http://localhost:8000/docs

## Demo Credentials

```
Email: admin@example.com
Password: admin123

Email: recruiter@example.com
Password: recruiter123

Email: manager@example.com
Password: manager123
```

## First API Call

1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Use Login endpoint with demo credentials
4. Copy the access_token
5. Click "Authorize" again and paste: `Bearer <token>`
6. Try the Candidates endpoint

## Project Layout

- **app/auth** - Login and registration
- **app/candidates** - Candidate profiles
- **app/jobs** - Job openings
- **app/applications** - Application tracking
- **app/ai** - AI-powered summaries
- **tests/** - Test suite

## Useful Commands

```bash
# Start services
docker-compose up

# Run tests
pytest tests/ -v

# View database
docker-compose exec db psql -U recruitment_user recruitment_db

# Stop services
docker-compose down
```

## Environment Configuration

Edit `.env` to:
- Change database connection
- Enable OpenAI provider
- Adjust token expiration
- Set production secret key

See `.env.example` for all options.
