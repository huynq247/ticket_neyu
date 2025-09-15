from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.service import verify_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = None):
    """
    Get current user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        User data if token is valid
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
        
    token = credentials.credentials
    user_data = await verify_token(token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token"
        )
        
    return user_data