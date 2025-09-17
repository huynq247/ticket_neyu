import os
from typing import List, Union, Optional
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Ticket Service"
    
    # Database configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://admin:Mypassword123@14.161.50.86:27017/content_db?authSource=admin")
    MONGODB_USER: str = os.getenv("MONGODB_USER", "admin")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD", "Mypassword123")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "content_db")
    MONGODB_AUTH_SOURCE: str = os.getenv("MONGODB_AUTH_SOURCE", "admin")
    
    # JWT configuration for token validation
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")  # Must match API Gateway
    
    # User Service URL
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://localhost:8000")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

settings = Settings()