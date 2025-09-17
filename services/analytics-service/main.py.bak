import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List

from app.core.config import settings
from app.api.endpoints import dashboard
from app.db.database import engine, SessionLocal
from app.models import sql_models
from app.etl.scheduler import start_etl_scheduler, stop_etl_scheduler

# Create database tables if they don't exist
sql_models.Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG_MODE else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Configure CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(
    dashboard.router,
    prefix=f"{settings.API_V1_STR}/dashboard",
    tags=["dashboard"],
)

@app.on_event("startup")
async def startup_event():
    """
    Initialize services on startup
    """
    logger.info("Starting up Analytics Service")
    # Start ETL scheduler
    start_etl_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up resources on shutdown
    """
    logger.info("Shutting down Analytics Service")
    # Stop ETL scheduler
    stop_etl_scheduler()

@app.get("/")
async def root():
    """
    Root endpoint for health check
    """
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "active"
    }

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=settings.DEBUG_MODE)