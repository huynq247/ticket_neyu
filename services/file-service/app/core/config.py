import os
import secrets
from typing import List, Optional, Union, Dict, Any

from pydantic import AnyHttpUrl, validator, BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "File Service"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # MongoDB Settings
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DB: str
    
    @property
    def MONGO_URI(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
    
    # File Storage Settings
    STORAGE_TYPE: str = "local"  # Options: local, s3, gridfs
    LOCAL_STORAGE_PATH: str = "./data/files"
    MAX_UPLOAD_SIZE: int = 104857600  # 100MB in bytes
    
    # Service URLs
    USER_SERVICE_URL: str
    TICKET_SERVICE_URL: str
    
    # JWT Settings
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()