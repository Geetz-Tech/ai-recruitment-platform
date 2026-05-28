from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import Base, engine
from .auth.router import router as auth_router
from .users.router import router as users_router
from .candidates.router import router as candidates_router
from .jobs.router import router as jobs_router
from .applications.router import router as applications_router
from .resumes.router import router as resumes_router
from .dashboard.router import router as dashboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="AI-Assisted Recruitment Workflow Platform API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(candidates_router)
app.include_router(jobs_router)
app.include_router(applications_router)
app.include_router(resumes_router)
app.include_router(dashboard_router)


@app.get("/")
async def root():
    return {"message": "AI-Assisted Recruitment Platform API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
