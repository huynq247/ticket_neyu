from fastapi import APIRouter
from app.api.endpoints import dashboard, time_analysis, user_analysis, custom_analysis

api_router = APIRouter()

# Include dashboard endpoints
api_router.include_router(
    dashboard.router, 
    prefix="/dashboard", 
    tags=["dashboard"]
)

# Include time analysis endpoints
api_router.include_router(
    time_analysis.router, 
    prefix="/time-analysis", 
    tags=["time-analysis"]
)

# Include user analysis endpoints
api_router.include_router(
    user_analysis.router, 
    prefix="/user-analysis", 
    tags=["user-analysis"]
)

# Include custom analysis endpoints
api_router.include_router(
    custom_analysis.router, 
    prefix="/custom-analysis", 
    tags=["custom-analysis"]
)