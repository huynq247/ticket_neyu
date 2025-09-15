from datetime import datetime
from typing import Dict, List, Optional, Any
from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING

from app.core.config import settings


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoDB:
    client = None
    db = None

    @classmethod
    def connect(cls):
        """Connect to MongoDB"""
        if cls.client is None:
            cls.client = MongoClient(settings.MONGODB_URI)
            cls.db = cls.client[settings.MONGODB_DATABASE]
            
            # Create indexes
            cls.db.tickets.create_index([("status", ASCENDING)])
            cls.db.tickets.create_index([("requester_id", ASCENDING)])
            cls.db.tickets.create_index([("assignee_id", ASCENDING)])
            cls.db.tickets.create_index([("category_id", ASCENDING)])
            cls.db.tickets.create_index([("created_at", DESCENDING)])
            
            cls.db.categories.create_index([("name", ASCENDING)], unique=True)
            
            cls.db.comments.create_index([("ticket_id", ASCENDING)])
            cls.db.comments.create_index([("created_at", DESCENDING)])
            
            print("MongoDB connected successfully")
        return cls.db

    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            cls.db = None
            print("MongoDB connection closed")


# Document models for MongoDB

class TicketDocument:
    """Ticket document model"""
    collection_name = "tickets"
    
    @staticmethod
    def get_collection():
        """Get tickets collection"""
        return MongoDB.connect()[TicketDocument.collection_name]
    
    @staticmethod
    def to_dict(ticket):
        """Convert ticket document to dict"""
        if not ticket:
            return None
        
        # Convert ObjectId to string
        ticket["id"] = str(ticket.pop("_id"))
        
        # Convert category_id to string if exists
        if "category_id" in ticket and ticket["category_id"]:
            ticket["category_id"] = str(ticket["category_id"])
        
        return ticket
    
    @staticmethod
    def from_dict(data):
        """Convert dict to ticket document"""
        if not data:
            return None
        
        # Convert id to ObjectId if exists
        if "id" in data:
            data["_id"] = ObjectId(data.pop("id"))
        
        # Convert category_id to ObjectId if exists
        if "category_id" in data and data["category_id"]:
            data["category_id"] = ObjectId(data["category_id"])
        
        return data


class CategoryDocument:
    """Category document model"""
    collection_name = "categories"
    
    @staticmethod
    def get_collection():
        """Get categories collection"""
        return MongoDB.connect()[CategoryDocument.collection_name]
    
    @staticmethod
    def to_dict(category):
        """Convert category document to dict"""
        if not category:
            return None
        
        # Convert ObjectId to string
        category["id"] = str(category.pop("_id"))
        
        return category
    
    @staticmethod
    def from_dict(data):
        """Convert dict to category document"""
        if not data:
            return None
        
        # Convert id to ObjectId if exists
        if "id" in data:
            data["_id"] = ObjectId(data.pop("id"))
        
        return data


class CommentDocument:
    """Comment document model"""
    collection_name = "comments"
    
    @staticmethod
    def get_collection():
        """Get comments collection"""
        return MongoDB.connect()[CommentDocument.collection_name]
    
    @staticmethod
    def to_dict(comment):
        """Convert comment document to dict"""
        if not comment:
            return None
        
        # Convert ObjectId to string
        comment["id"] = str(comment.pop("_id"))
        
        # Convert ticket_id to string if exists
        if "ticket_id" in comment and comment["ticket_id"]:
            comment["ticket_id"] = str(comment["ticket_id"])
        
        return comment
    
    @staticmethod
    def from_dict(data):
        """Convert dict to comment document"""
        if not data:
            return None
        
        # Convert id to ObjectId if exists
        if "id" in data:
            data["_id"] = ObjectId(data.pop("id"))
        
        # Convert ticket_id to ObjectId if exists
        if "ticket_id" in data and data["ticket_id"]:
            data["ticket_id"] = ObjectId(data["ticket_id"])
        
        return data