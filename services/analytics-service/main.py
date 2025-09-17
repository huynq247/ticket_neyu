from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import sys
from sqlalchemy.orm import Session

# Create a simple health check endpoint first, before any imports that might fail
app = FastAPI(
    title="Analytics Service",
    description="Analytics Service API for Ticket Management System",
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
    return {"status": "ok", "service": "analytics-service"}

try:
    # Only import these if possible
    from app.api.api import api_router
    from app.core.config import settings
    from app.db.database import get_db, get_mongodb_client
    
    # Include API router
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/db-check")
    def db_check(db: Session = Depends(get_db)):
        """Database connection check"""
        result = {"databases": []}
        
        # Check PostgreSQL connection
        try:
            # Execute a simple query to verify database connection
            db.execute("SELECT 1")
            result["databases"].append({"name": "PostgreSQL", "status": "ok", "message": "Connected successfully"})
        except Exception as e:
            result["databases"].append({"name": "PostgreSQL", "status": "error", "message": str(e)})
        
        # Check MongoDB connection
        try:
            mongo_client = get_mongodb_client()
            mongo_db = mongo_client[settings.MONGODB_DATABASE]
            mongo_db.command("ping")
            result["databases"].append({"name": "MongoDB", "status": "ok", "message": "Connected successfully"})
        except Exception as e:
            result["databases"].append({"name": "MongoDB", "status": "error", "message": str(e)})
        
        # Overall status
        if all(db["status"] == "ok" for db in result["databases"]):
            result["status"] = "ok"
        else:
            result["status"] = "error"
            
        return result
except Exception as e:
    print(f"Warning: Could not load full API: {e}")
    print("Analytics service will run in limited mode")
    
    @app.get("/api/v1/status")
    def api_status():
        return {
            "status": "limited", 
            "message": "Analytics service is running in limited mode due to dependency issues",
            "error": str(e)
        }
    
    @app.get("/db-check")
    def db_check():
        """Database connection check"""
        return {"status": "error", "message": "Service is running in limited mode, database unavailable", "error": str(e)}

if __name__ == "__main__":
    try:
        print("Starting Analytics Service on port 8005...")
        uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
    except Exception as e:
        print(f"Error starting server: {e}")
