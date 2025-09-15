from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, Generator
import jwt
from datetime import datetime, timedelta
import httpx
import json

from app.db.database import get_db
from app.core.config import settings

# OAuth2 scheme for token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.USER_SERVICE_URL}/api/auth/login")

# Database dependency
def get_db_session() -> Generator:
    """
    Get database session
    """
    return get_db()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Validate JWT token and get current user from User Service
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Get user details from User Service
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(
                f"{settings.USER_SERVICE_URL}/api/users/me", 
                headers=headers
            )
            
            if response.status_code != 200:
                raise credentials_exception
            
            user_data = response.json()
            return user_data
            
    except jwt.PyJWTError:
        raise credentials_exception

def get_service_token() -> str:
    """
    Generate a service-to-service JWT token for internal communication
    """
    expiration = datetime.utcnow() + timedelta(minutes=5)  # Short-lived token
    
    payload = {
        "sub": "analytics-service",
        "service": True,
        "exp": expiration,
        "api_key": settings.SERVICE_API_KEY
    }
    
    token = jwt.encode(
        payload, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token

async def validate_service_api_key(
    x_api_key: Optional[str] = Header(None)
) -> None:
    """
    Validate service API key for service-to-service communication
    """
    if not x_api_key or x_api_key != settings.SERVICE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )