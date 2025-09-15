from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import sys

# Create a simple health check endpoint first, before any imports that might fail
app = FastAPI(
    title="Report Service",
    description="Report Service API for Ticket Management System",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "report-service"}

try:
    # Only import these if possible
    from app.api.api import api_router
    from app.core.config import settings
    
    # Include API router
    app.include_router(api_router, prefix="/api/v1")
except Exception as e:
    print(f"Warning: Could not load full API: {e}")
    print("Report service will run in limited mode")
    
    @app.get("/api/v1/status")
    def api_status():
        return {
            "status": "limited", 
            "message": "Report service is running in limited mode due to dependency issues",
            "error": str(e)
        }

if __name__ == "__main__":
    try:
        print("Starting Report Service on port 8004...")
        uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
    except Exception as e:
        print(f"Error starting server: {e}")
