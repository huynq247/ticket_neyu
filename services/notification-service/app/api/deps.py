from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
from typing import Dict, Any, Optional
import httpx
import os

from app.core.config import settings

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Validate token and get current user from User Service
    """
    try:
        # Extract token from authorization header
        token = credentials.credentials
        
        # First, verify token validity locally
        try:
            # Just verify the token signature and expiration
            payload = jwt.decode(
                token, 
                settings.JWT_PUBLIC_KEY, 
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_signature": True}
            )
        except PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}"
            )
        
        # Then, validate with User Service to ensure user exists and token is not revoked
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.USER_SERVICE_URL}/api/users/me",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User authentication failed"
                    )
                
                return response.json()
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service unavailable"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}"
        )