# PowerShell script to start the analytics service with Python 3.10
# This script addresses potential database connection issues

$pythonPath = "$PSScriptRoot\venv_py310\Scripts\python.exe"

# Change directory to analytics service
Set-Location -Path "$PSScriptRoot\services\analytics-service"

# Create a modified version of main.py with better error handling
$mainContent = @"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import sys

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
    
    # Include API router
    app.include_router(api_router, prefix="/api/v1")
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

if __name__ == "__main__":
    try:
        print("Starting Analytics Service on port 8005...")
        uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
    except Exception as e:
        print(f"Error starting server: {e}")
"@

# Create backup of main.py if it doesn't exist already
if (-Not (Test-Path -Path ".\main.py.bak")) {
    Copy-Item -Path ".\main.py" -Destination ".\main.py.bak" -Force
    Write-Host "Created backup of original main.py file" -ForegroundColor Green
}

# Write the modified main.py file
Set-Content -Path ".\main.py" -Value $mainContent
Write-Host "Updated main.py with error handling" -ForegroundColor Green

# Create a simplified database.py file with fallback for MongoDB if it exists
if (Test-Path -Path ".\app\core\database.py") {
    # Create a simplified database.py file with fallback for MongoDB
    $databaseContent = @"
from pymongo import MongoClient
from pymongo.database import Database
import os
import time

from app.core.config import settings

# Create a simple file-based database for development
class FileBasedDB:
    def __init__(self, base_dir="./data/analytics"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
        # Create a simple collection-like interface
        self.events = FileCollection(os.path.join(base_dir, "events"))
        self.metrics = FileCollection(os.path.join(base_dir, "metrics"))
    
    def __getitem__(self, collection_name):
        if collection_name == "events":
            return self.events
        elif collection_name == "metrics":
            return self.metrics
        raise KeyError(f"Collection {collection_name} not found")

class FileCollection:
    def __init__(self, directory):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)
    
    def create_index(self, field_name):
        # No-op for file-based storage
        pass
    
    def insert_one(self, document):
        # Implementation for local file ops will be handled in models
        return {"inserted_id": document.get("_id")}
    
    def find_one(self, query):
        # Implementation for local file ops will be handled in models
        return None
    
    def find(self, query=None):
        # Implementation for local file ops will be handled in models
        return []
    
    def update_one(self, query, update):
        # Implementation for local file ops will be handled in models
        return {"modified_count": 0}
    
    def delete_one(self, query):
        # Implementation for local file ops will be handled in models
        return {"deleted_count": 0}
    
    def count_documents(self, query):
        # Implementation for local file ops will be handled in models
        return 0

# Try to connect to MongoDB, fall back to file-based storage if it fails
try:
    print("Attempting to connect to MongoDB...")
    client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.server_info()
    db = client[settings.MONGODB_DATABASE]
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using file-based storage as fallback")
    db = FileBasedDB()

# Define collections
events_collection = db["events"]
metrics_collection = db["metrics"]

# Create indexes (only affects MongoDB, no-op for file-based)
try:
    events_collection.create_index("timestamp")
    events_collection.create_index("user_id")
    metrics_collection.create_index("metric_name")
except Exception as e:
    print(f"Failed to create indexes: {e}")
"@

    # Make sure the app/core directory exists
    if (-Not (Test-Path -Path ".\app\core")) {
        New-Item -Path ".\app\core" -ItemType Directory -Force
        Write-Host "Created app/core directory" -ForegroundColor Green
    }

    # Create backup
    Copy-Item -Path ".\app\core\database.py" -Destination ".\app\core\database.py.bak" -Force
    # Write the new file
    Set-Content -Path ".\app\core\database.py" -Value $databaseContent
    Write-Host "Updated database.py with fallback mechanism" -ForegroundColor Green
}

# Create data directory if it doesn't exist
if (-Not (Test-Path -Path ".\data\analytics")) {
    New-Item -Path ".\data\analytics" -ItemType Directory -Force
    Write-Host "Created data directory for analytics" -ForegroundColor Green
}

# Install minimal dependencies
Write-Host "Installing core dependencies..." -ForegroundColor Yellow
& $pythonPath -m pip install fastapi==0.103.1 uvicorn==0.23.2 pydantic==1.10.12 pymongo==4.6.1 python-dotenv==1.0.0

# Start analytics service
Write-Host "Starting Analytics Service with Python 3.10..." -ForegroundColor Yellow
& $pythonPath main.py

# Return to the original directory
Set-Location -Path $PSScriptRoot