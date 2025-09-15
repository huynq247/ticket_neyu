from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
db: Database = client[settings.MONGO_DB]

# Define collections
notification_collection = db["notifications"]
template_collection = db["templates"]

# Create indexes
notification_collection.create_index("recipient_id")
notification_collection.create_index("status")
notification_collection.create_index("created_at")
template_collection.create_index("name", unique=True)