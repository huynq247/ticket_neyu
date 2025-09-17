from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import redis
import logging
from typing import Generator, Any

from app.core.config import settings, DATABASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy PostgreSQL setup for Data Warehouse
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB connection for unstructured analytics data
_mongo_client = None

def get_mongodb_client() -> MongoClient:
    """
    Create or return existing MongoDB client
    """
    global _mongo_client
    if _mongo_client is None:
        try:
            mongo_url = settings.MONGODB_URL
            print(f"Attempting to connect to MongoDB with URL: {mongo_url}")
            _mongo_client = MongoClient(mongo_url)
            # Test connection
            _mongo_client.server_info()
            print("Successfully connected to MongoDB")
            logger.info("MongoDB connection established")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    return _mongo_client

# Redis connection for caching
_redis_client = None

def get_redis_client():
    """
    Create or return existing Redis client
    """
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.from_url(settings.REDIS_URL)
            # Test connection
            _redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    return _redis_client

def get_db() -> Generator:
    """
    Get database session for PostgreSQL
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """
    Initialize the PostgreSQL database, creating tables if they don't exist
    """
    try:
        # Create all tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing PostgreSQL database: {e}")
        raise