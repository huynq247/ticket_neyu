from fastapi import APIRouter

from app.api.endpoints import (
    reports,
    templates,
    dashboards,
    scheduled_reports,
    report_execution
)

api_router = APIRouter()

# Reports endpoints
api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["reports"]
)

# Templates endpoints
api_router.include_router(
    templates.router,
    prefix="/templates",
    tags=["templates"]
)

# Dashboards endpoints
api_router.include_router(
    dashboards.router,
    prefix="/dashboards",
    tags=["dashboards"]
)

# Scheduled reports endpoints
api_router.include_router(
    scheduled_reports.router,
    prefix="/scheduled-reports",
    tags=["scheduled-reports"]
)

# Report execution endpoints
api_router.include_router(
    report_execution.router,
    prefix="/execute",
    tags=["report-execution"]
)