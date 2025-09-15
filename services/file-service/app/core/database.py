from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
db: Database = client[settings.MONGO_DB]

# Define collections
file_collection = db["files"]

# Create indexes
file_collection.create_index("filename")
file_collection.create_index("owner_id")
file_collection.create_index("ticket_id")