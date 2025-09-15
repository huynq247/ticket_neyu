from fastapi import APIRouter

from app.api.endpoints import (
    dashboard,
    time_analysis,
    user_analysis,
    custom_analysis
)

router = APIRouter()

router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
router.include_router(time_analysis.router, prefix="/time", tags=["time-analysis"])
router.include_router(user_analysis.router, prefix="/users", tags=["user-analysis"])
router.include_router(custom_analysis.router, prefix="/custom", tags=["custom-analysis"])