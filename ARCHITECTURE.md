# Architecture Overview

## System Design Principles

This project follows clean architecture principles with clear separation of concerns:

### Layer Structure

```
┌─────────────────────────────────────────┐
│         API Layer (Routers)             │
│    - HTTP endpoints and request handling │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       Business Logic (Services)          │
│    - Domain logic and operations         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Data Access (Models + Database)    │
│    - SQLAlchemy ORM and queries         │
└─────────────────────────────────────────┘
```

## Module Organization

### Core (`app/core/`)
- **config.py**: Environment configuration with Pydantic Settings
- **database.py**: SQLAlchemy session management and Base declarative class
- **security.py**: JWT and password hashing utilities
- **dependencies.py**: FastAPI dependency injection for auth and role checks

### Domain Modules
Each domain module (auth, users, candidates, jobs, etc.) follows a consistent pattern:

```
module/
├── __init__.py
├── models.py      # SQLAlchemy ORM models
├── schemas.py     # Pydantic request/response schemas
├── router.py      # FastAPI routes and endpoints
└── service.py     # Business logic and database operations
```

### Supporting Modules

**audit/**: Activity logging and candidate notes
- Tracks all state changes for compliance
- Captures user actions and timestamps

**ai/**: AI-powered candidate summaries
- Abstract provider pattern
- Mock provider (default)
- OpenAI provider (configurable)

**dashboard/**: Analytics and metrics
- Summary statistics
- Grouped aggregations
- Performance queries

**resumes/**: File handling
- Resume upload validation
- Metadata storage
- Document type checking

## Key Architectural Patterns

### Dependency Injection
FastAPI's dependency system is used for:
- Database session management
- Authentication and authorization
- Consistent error handling

```python
async def endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass
```

### Service Layer
All business logic is contained in service classes:
- Database operations
- Data validation
- Business rules enforcement

```python
class CandidateService:
    @staticmethod
    def create_candidate(db: Session, candidate: CandidateCreate) -> Candidate:
        # Business logic here
        pass
```

### Pydantic Schemas
Request/response validation is strict:
- Input validation at endpoint boundary
- Type safety with type hints
- Automatic API documentation

### Provider Pattern
AI integration uses an extensible provider pattern:
- MockAIProvider: Default, requires no API keys
- OpenAIProvider: Optional, uses OpenAI API
- Easy to add new providers

## Authentication & Authorization

### JWT-Based Auth
- Tokens include user ID in subject claim
- Configurable expiration (default: 30 minutes)
- No refresh tokens (stateless design)

### Role-Based Access Control
```python
@router.post("")
async def create_job(
    job: JobOpeningCreate,
    current_user: User = Depends(require_role("admin", "hiring_manager")),
):
    pass
```

Three roles:
- **admin**: Full system access
- **recruiter**: Candidate and application management
- **hiring_manager**: Job and application management

## Database Design

### Normalization
Tables follow 3NF principles:
- Clear primary keys
- Foreign key relationships
- Referential integrity constraints

### Timestamps
All records include:
- `created_at`: Server-generated, immutable
- `updated_at`: Auto-updated on modification

### Enums
Status fields use PostgreSQL ENUMs for:
- Data integrity
- Query optimization
- Type safety in code

## Error Handling

Consistent HTTP status codes:
- 200/201: Success
- 400: Bad request (validation, duplicates)
- 401: Unauthorized (invalid token)
- 403: Forbidden (insufficient permissions)
- 404: Not found
- 500: Server error

## Testing Strategy

### Unit Tests
- Auth flow (register, login)
- Candidate CRUD operations
- Job creation and updates

### Test Database
SQLite in-memory database for speed and isolation

### Fixtures
Centralized test setup in conftest.py

## Deployment Considerations

### Docker
- Multi-stage builds possible
- Environment variables for configuration
- Health checks for orchestration

### Database Migrations
- Alembic for version control
- Reversible migrations
- Can be run automatically on startup

### Scaling Notes
- Stateless design (JWT tokens)
- Database connection pooling
- Can run multiple API instances behind load balancer
- No session affinity required

## Future Extension Points

1. **Authentication**: Add OAuth2, SAML, LDAP providers
2. **Notifications**: Email, Slack, in-app messaging
3. **Search**: Elasticsearch for advanced candidate search
4. **Async Tasks**: Celery for background jobs
5. **Caching**: Redis for frequently accessed data
6. **Analytics**: Data warehouse integration
7. **Frontend**: React/Vue application
8. **Real-time**: WebSocket for live notifications

## Performance Considerations

- Database indexes on frequently queried columns
- Pagination for list endpoints
- Query optimization for aggregations
- Connection pooling for database access
- Configurable AI provider for cost optimization
