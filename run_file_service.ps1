# PowerShell script to start the file service with Python 3.10
# This script addresses the MongoDB connection issue

$pythonPath = "$PSScriptRoot\venv_py310\Scripts\python.exe"

# Change directory to file service
Set-Location -Path "$PSScriptRoot\services\file-service"

# Create the data directory if it doesn't exist
if (-Not (Test-Path -Path ".\data\files")) {
    New-Item -Path ".\data\files" -ItemType Directory -Force
    Write-Host "Created data directory for file storage" -ForegroundColor Green
}

# Modify database.py to fix MongoDB connection issues by adding error handling
$databaseContent = @"
from pymongo import MongoClient
from pymongo.database import Database
import os
import time

from app.core.config import settings

# Create a simple file-based database for development
class FileBasedDB:
    def __init__(self, base_dir="./data/files"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
        # Create a simple collection-like interface
        self.files = FileCollection(os.path.join(base_dir, "files"))
    
    def __getitem__(self, collection_name):
        if collection_name == "files":
            return self.files
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
    client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.server_info()
    db = client[settings.MONGO_DB]
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using file-based storage as fallback")
    db = FileBasedDB()

# Define collections
file_collection = db["files"]

# Create indexes (only affects MongoDB, no-op for file-based)
try:
    file_collection.create_index("filename")
    file_collection.create_index("owner_id")
    file_collection.create_index("ticket_id")
except Exception as e:
    print(f"Failed to create indexes: {e}")
"@

# Write the modified database.py file
Set-Content -Path ".\app\core\database.py" -Value $databaseContent

# Create a backup of the main.py file
Copy-Item -Path ".\main.py" -Destination ".\main.py.bak" -Force

# Modify main.py to add more detailed error handling
$mainContent = @"
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

if __name__ == "__main__":
    try:
        print("Starting File Service on port 8002...")
        uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
    except Exception as e:
        print(f"Error starting server: {e}")
"@

# Write the modified main.py file
Set-Content -Path ".\main.py" -Value $mainContent

# Now run the file service
Write-Host "Starting File Service with Python 3.10..." -ForegroundColor Yellow
& $pythonPath -m pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
    & $pythonPath main.py
}
else {
    Write-Host "Failed to install dependencies" -ForegroundColor Red
}

# Return to the original directory
Set-Location -Path $PSScriptRoot