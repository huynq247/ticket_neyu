from pymongo import MongoClient
from pymongo.database import Database
import os
import time

from app.core.config import settings

# Create a simple file-based database for development
class FileBasedDB:
    def __init__(self, base_dir="./data/reports"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
        # Create a simple collection-like interface
        self.reports = FileCollection(os.path.join(base_dir, "reports"))
        self.templates = FileCollection(os.path.join(base_dir, "templates"))
    
    def __getitem__(self, collection_name):
        if collection_name == "reports":
            return self.reports
        elif collection_name == "templates":
            return self.templates
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
report_collection = db["reports"]
template_collection = db["templates"]

# Create indexes (only affects MongoDB, no-op for file-based)
try:
    report_collection.create_index("user_id")
    report_collection.create_index("created_at")
    template_collection.create_index("name")
except Exception as e:
    print(f"Failed to create indexes: {e}")
