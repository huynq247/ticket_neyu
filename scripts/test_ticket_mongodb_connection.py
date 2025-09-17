"""
Test script to verify MongoDB connection from Ticket Service
"""
import os
import sys
from pymongo import MongoClient

# Add the ticket-service directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services', 'ticket-service'))

# Import settings from ticket-service
from app.core.config import settings

def test_mongodb_connection():
    """Test MongoDB connection using the Ticket Service configuration"""
    print(f"Attempting to connect to MongoDB at: {settings.MONGODB_URI}")
    
    try:
        # Create MongoDB client
        client = MongoClient(settings.MONGODB_URI)
        
        # Verify connection by listing databases
        dbs = client.list_database_names()
        print(f"Successfully connected to MongoDB. Available databases: {dbs}")
        
        # Check if the content_db database exists
        if settings.MONGODB_DATABASE in dbs:
            print(f"Database '{settings.MONGODB_DATABASE}' exists")
            
            # Connect to the database
            db = client[settings.MONGODB_DATABASE]
            
            # List collections
            collections = db.list_collection_names()
            print(f"Collections in {settings.MONGODB_DATABASE}: {collections}")
            
            # Count documents in tickets collection if it exists
            if "tickets" in collections:
                ticket_count = db.tickets.count_documents({})
                print(f"Number of documents in tickets collection: {ticket_count}")
        else:
            print(f"Database '{settings.MONGODB_DATABASE}' does not exist yet")
        
        return True
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    if success:
        print("MongoDB connection test passed!")
        sys.exit(0)
    else:
        print("MongoDB connection test failed!")
        sys.exit(1)