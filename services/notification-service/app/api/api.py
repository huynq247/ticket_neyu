from fastapi import APIRouter
from app.api.endpoints import notifications, templates

api_router = APIRouter()

# Include notification endpoints
api_router.include_router(
    notifications.router, 
    prefix="/notifications", 
    tags=["notifications"]
)

# Include template endpoints
api_router.include_router(
    templates.router, 
    prefix="/templates", 
    tags=["templates"]
)