from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import sys

# Create data directory if it doesn't exist
os.makedirs("./data/files", exist_ok=True)

try:
    from app.api.api import api_router
    from app.core.config import settings
    from app.core.database import client, db
except Exception as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

app = FastAPI(
    title="File Service",
    description="File Service API for Ticket Management System",
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

# Include API router
try:
    app.include_router(api_router, prefix="/api/v1")
except Exception as e:
    print(f"Error including API router: {e}")

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "file-service"}

@app.get("/db-check")
def db_check():
    """Database connection check"""
    try:
        # Check if we're using MongoDB or file-based fallback
        if hasattr(db, "command"):
            # This is a MongoDB connection
            db.command("ping")
            return {"status": "ok", "message": "MongoDB connection successful", "storage_type": "mongodb"}
        else:
            # This is the file-based fallback
            return {"status": "warning", "message": "Using file-based storage fallback", "storage_type": "file"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}

@app.get("/test")
def test_endpoint():
    """Test endpoint to verify changes are applied"""
    return {"status": "ok", "message": "Test endpoint is working", "time": "now"}

if __name__ == "__main__":
    try:
        print("Starting File Service on port 8002...")
        uvicorn.run("main_new:app", host="0.0.0.0", port=8002, reload=True)
    except Exception as e:
        print(f"Error starting server: {e}")