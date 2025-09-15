from typing import Dict, Any
import pymongo
import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# MongoDB Connection
mongo_client = pymongo.MongoClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB]

# Report collections
report_collection = mongo_db["reports"]
report_template_collection = mongo_db["report_templates"]
dashboard_collection = mongo_db["dashboards"]
scheduled_report_collection = mongo_db["scheduled_reports"]

# Create indices for better performance
report_collection.create_index([("created_by", pymongo.ASCENDING)])
report_collection.create_index([("created_at", pymongo.DESCENDING)])
report_template_collection.create_index([("name", pymongo.ASCENDING)], unique=True)
dashboard_collection.create_index([("created_by", pymongo.ASCENDING)])
scheduled_report_collection.create_index([("next_run", pymongo.ASCENDING)])

# PostgreSQL Connection (Read-only for reporting)
sqlalchemy_engine = create_engine(
    settings.POSTGRES_URI,
    pool_pre_ping=True,
    connect_args={"options": "-c statement_timeout=30000"}  # 30 seconds timeout
)
SqlAlchemySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlalchemy_engine)
SqlAlchemyBase = declarative_base()

# Redis Connection (for caching)
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Helper functions
def get_db_session():
    """
    Get a PostgreSQL database session
    """
    db = SqlAlchemySessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_report(report_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a report to MongoDB
    """
    result = report_collection.insert_one(report_data)
    return report_collection.find_one({"_id": result.inserted_id})


def save_report_template(template_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a report template to MongoDB
    """
    result = report_template_collection.insert_one(template_data)
    return report_template_collection.find_one({"_id": result.inserted_id})


def save_dashboard(dashboard_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a dashboard to MongoDB
    """
    result = dashboard_collection.insert_one(dashboard_data)
    return dashboard_collection.find_one({"_id": result.inserted_id})


def save_scheduled_report(scheduled_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a scheduled report to MongoDB
    """
    result = scheduled_report_collection.insert_one(scheduled_data)
    return scheduled_report_collection.find_one({"_id": result.inserted_id})