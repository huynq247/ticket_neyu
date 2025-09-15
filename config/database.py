"""
Database configuration and connection utilities.
This module provides functions to connect to MongoDB and PostgreSQL databases
using configuration from environment variables or .env files.
"""

import os
from dotenv import load_dotenv
import motor.motor_asyncio
from pymongo import MongoClient
import asyncpg
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

# Load environment variables from .env file
load_dotenv("config/database.env")

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/ticket_system")
MONGODB_USER = os.getenv("MONGODB_USER", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "ticket_system")
MONGODB_AUTH_SOURCE = os.getenv("MONGODB_AUTH_SOURCE", "admin")

# PostgreSQL Configuration
POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://localhost:5432/users")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "users")

# Redis Configuration
REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379/0")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# SQLAlchemy setup
Base = declarative_base()

def get_mongodb_uri():
    """
    Get MongoDB URI with authentication if credentials are provided.
    
    Returns:
        str: MongoDB connection URI
    """
    if MONGODB_USER and MONGODB_PASSWORD:
        # Parse existing URI to extract host and port
        parts = MONGODB_URI.split("//")[1].split("/")
        host_port = parts[0]
        db_name = parts[1] if len(parts) > 1 else MONGODB_DATABASE
        
        # Construct URI with authentication
        return f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{host_port}/{db_name}?authSource={MONGODB_AUTH_SOURCE}"
    
    return MONGODB_URI

def get_postgres_uri():
    """
    Get PostgreSQL URI with authentication if credentials are provided.
    
    Returns:
        str: PostgreSQL connection URI
    """
    if POSTGRES_USER and POSTGRES_PASSWORD:
        # Parse existing URI to extract host and port
        parts = POSTGRES_URI.split("//")[1].split("/")
        host_port = parts[0]
        db_name = parts[1] if len(parts) > 1 else POSTGRES_DATABASE
        
        # Construct URI with authentication
        return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{host_port}/{db_name}"
    
    return POSTGRES_URI

def get_redis_uri():
    """
    Get Redis URI with authentication if password is provided.
    
    Returns:
        str: Redis connection URI
    """
    if REDIS_PASSWORD:
        # Parse existing URI to extract host, port and db
        parts = REDIS_URI.split("//")[1].split("/")
        host_port = parts[0]
        db = parts[1] if len(parts) > 1 else "0"
        
        # Construct URI with authentication
        return f"redis://:{REDIS_PASSWORD}@{host_port}/{db}"
    
    return REDIS_URI

# MongoDB Connection Functions
def get_mongodb_client():
    """
    Get a synchronous MongoDB client.
    
    Returns:
        pymongo.MongoClient: MongoDB client
    """
    return MongoClient(get_mongodb_uri())

def get_mongodb_database():
    """
    Get a synchronous MongoDB database.
    
    Returns:
        pymongo.database.Database: MongoDB database
    """
    client = get_mongodb_client()
    return client[MONGODB_DATABASE]

async def get_async_mongodb_client():
    """
    Get an asynchronous MongoDB client.
    
    Returns:
        motor.motor_asyncio.AsyncIOMotorClient: Async MongoDB client
    """
    return motor.motor_asyncio.AsyncIOMotorClient(get_mongodb_uri())

async def get_async_mongodb_database():
    """
    Get an asynchronous MongoDB database.
    
    Returns:
        motor.motor_asyncio.AsyncIOMotorDatabase: Async MongoDB database
    """
    client = await get_async_mongodb_client()
    return client[MONGODB_DATABASE]

# PostgreSQL Connection Functions
def get_postgres_connection():
    """
    Get a synchronous PostgreSQL connection.
    
    Returns:
        psycopg2.connection: PostgreSQL connection
    """
    return psycopg2.connect(
        dbname=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_URI.split("//")[1].split(":")[0],
        port=int(POSTGRES_URI.split("//")[1].split(":")[1].split("/")[0])
    )

def get_sqlalchemy_engine():
    """
    Get a SQLAlchemy engine for PostgreSQL.
    
    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine
    """
    return create_engine(get_postgres_uri())

def get_sqlalchemy_session_maker():
    """
    Get a SQLAlchemy session maker.
    
    Returns:
        sqlalchemy.orm.session.sessionmaker: Session maker
    """
    engine = get_sqlalchemy_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_async_postgres_connection():
    """
    Get an asynchronous PostgreSQL connection.
    
    Returns:
        asyncpg.Connection: Async PostgreSQL connection
    """
    uri = get_postgres_uri()
    return await asyncpg.connect(uri)

# Redis Connection Functions
def get_redis_client():
    """
    Get a Redis client.
    
    Returns:
        redis.Redis: Redis client
    """
    return redis.from_url(get_redis_uri())

# Test connections
def test_connections():
    """
    Test connections to all databases.
    
    Returns:
        dict: Connection status for each database
    """
    status = {}
    
    # Test MongoDB
    try:
        client = get_mongodb_client()
        client.server_info()
        status["mongodb"] = "Connected"
    except Exception as e:
        status["mongodb"] = f"Error: {str(e)}"
    
    # Test PostgreSQL
    try:
        conn = get_postgres_connection()
        conn.close()
        status["postgres"] = "Connected"
    except Exception as e:
        status["postgres"] = f"Error: {str(e)}"
    
    # Test Redis
    try:
        client = get_redis_client()
        client.ping()
        status["redis"] = "Connected"
    except Exception as e:
        status["redis"] = f"Error: {str(e)}"
    
    return status

if __name__ == "__main__":
    # Print connection status when run directly
    status = test_connections()
    for db, status in status.items():
        print(f"{db}: {status}")