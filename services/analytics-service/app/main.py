from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Analytics Service",
    description="Advanced analytics and visualization for ticket data",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)

@app.get("/")
async def root():
    """
    Root endpoint returning service information
    """
    return {
        "service": "Analytics Service",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Analytics Service")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)