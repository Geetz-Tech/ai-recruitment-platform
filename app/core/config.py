from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "AI-Assisted Recruitment Platform"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:password@localhost/recruitment_db"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Service
    ai_provider: str = "mock"  # Options: mock, openai
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
