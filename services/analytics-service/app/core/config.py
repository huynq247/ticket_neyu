import os
from typing import List, Union, Optional, Dict, Any
from pydantic import AnyHttpUrl, validator, BaseSettings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # Service Configuration
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Analytics Service")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "Analytics Service for Ticket Management System")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "True") == "True"
    API_V1_STR: str = os.getenv("API_V1_STR", "/api")
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-super-secret-key-here")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    SERVICE_API_KEY: str = os.getenv("SERVICE_API_KEY", "your-service-api-key-here")
    
    # Database - PostgreSQL (Data Warehouse)
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "analytics_service")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    # Database - MongoDB (for unstructured analytics data)
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "analytics_service")
    
    # Redis for caching
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_TTL: int = int(os.getenv("REDIS_TTL", "3600"))
    
    # Service URLs
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://localhost:8000")
    TICKET_SERVICE_URL: str = os.getenv("TICKET_SERVICE_URL", "http://localhost:8001")
    FILE_SERVICE_URL: str = os.getenv("FILE_SERVICE_URL", "http://localhost:8002")
    NOTIFICATION_SERVICE_URL: str = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8003")
    REPORT_SERVICE_URL: str = os.getenv("REPORT_SERVICE_URL", "http://localhost:8004")
    ANALYTICS_SERVICE_URL: str = os.getenv("ANALYTICS_SERVICE_URL", "http://localhost:8005")
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # ETL Configuration
    ETL_SCHEDULE_INTERVAL: int = int(os.getenv("ETL_SCHEDULE_INTERVAL", "3600"))
    ETL_BATCH_SIZE: int = int(os.getenv("ETL_BATCH_SIZE", "1000"))
    
    # Storage
    DATA_WAREHOUSE_RETENTION_DAYS: int = int(os.getenv("DATA_WAREHOUSE_RETENTION_DAYS", "730"))
    
    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()

# Database connection string for PostgreSQL
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"