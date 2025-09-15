import httpx
from typing import Dict, Any, Optional

from app.core.config import settings


async def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT token with User Service
    
    Args:
        token: JWT token to verify
        
    Returns:
        User data if token is valid, None otherwise
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.USER_SERVICE_URL}/api/v1/auth/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
        except Exception:
            return None


async def check_file_permission(user_id: str, ticket_id: Optional[str]) -> bool:
    """
    Check if user has permission to access a ticket's files
    
    Args:
        user_id: ID of the user
        ticket_id: ID of the ticket
        
    Returns:
        True if user has permission, False otherwise
    """
    if not ticket_id:
        return True
        
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.TICKET_SERVICE_URL}/api/v1/tickets/{ticket_id}/access",
                params={"user_id": user_id}
            )
            
            if response.status_code == 200:
                return response.json().get("has_access", False)
            
            return False
        except Exception:
            return False