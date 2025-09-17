"""
Compatibility module to redirect imports from app.db.database to app.core.database
"""

# Re-export everything from app.core.database
from app.core.database import *
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB client singleton
_mongo_client = None

def get_mongodb_client() -> MongoClient:
    """
    Create or return existing MongoDB client
    """
    global _mongo_client
    if _mongo_client is None:
        try:
            from app.core.config import settings
            mongo_url = settings.MONGO_URI + "?authSource=admin"
            print(f"Get MongoDB Client - Attempting to connect with URL: {mongo_url}")
            _mongo_client = MongoClient(mongo_url)
            # Test connection
            _mongo_client.server_info()
            print("Get MongoDB Client - Successfully connected")
            logger.info("MongoDB connection established")
        except Exception as e:
            print(f"Get MongoDB Client - Connection failed: {e}")
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    return _mongo_client