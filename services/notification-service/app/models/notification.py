from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.core.database import notification_collection
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationStatus


def create_notification(notification_data: NotificationCreate) -> Dict[str, Any]:
    """
    Create a new notification record in the database
    
    Args:
        notification_data: Notification data
        
    Returns:
        Created notification document
    """
    notification_dict = notification_data.model_dump()
    
    # Add additional fields
    notification_dict["status"] = (
        NotificationStatus.SCHEDULED 
        if notification_data.scheduled_for 
        else NotificationStatus.PENDING
    )
    notification_dict["created_at"] = datetime.utcnow()
    notification_dict["updated_at"] = datetime.utcnow()
    
    # Insert into database
    result = notification_collection.insert_one(notification_dict)
    
    # Get the inserted document
    return get_notification(result.inserted_id)


def get_notification(notification_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a notification by ID
    
    Args:
        notification_id: ID of the notification
        
    Returns:
        Notification document if found, None otherwise
    """
    if isinstance(notification_id, str):
        try:
            notification_id = ObjectId(notification_id)
        except:
            return None
            
    return notification_collection.find_one({"_id": notification_id})


def update_notification(notification_id: str, update_data: NotificationUpdate) -> Optional[Dict[str, Any]]:
    """
    Update a notification record
    
    Args:
        notification_id: ID of the notification to update
        update_data: New data for the notification
        
    Returns:
        Updated notification document if found and updated, None otherwise
    """
    notification = get_notification(notification_id)
    if not notification:
        return None
        
    # Convert to ObjectId
    if isinstance(notification_id, str):
        notification_id = ObjectId(notification_id)
    
    # Prepare update data
    update_dict = update_data.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    # Update in database
    notification_collection.update_one(
        {"_id": notification_id},
        {"$set": update_dict}
    )
    
    # Return updated document
    return get_notification(notification_id)


def list_notifications(
    skip: int = 0,
    limit: int = 100,
    recipient_id: Optional[str] = None,
    status: Optional[NotificationStatus] = None,
    notification_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List notifications with filtering options
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        recipient_id: Filter by recipient ID
        status: Filter by status
        notification_type: Filter by notification type
        
    Returns:
        List of notification documents
    """
    # Build query
    query = {}
    
    if recipient_id:
        query["recipient_id"] = recipient_id
        
    if status:
        query["status"] = status
        
    if notification_type:
        query["notification_type"] = notification_type
        
    # Execute query
    cursor = notification_collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    
    return list(cursor)


def count_notifications(
    recipient_id: Optional[str] = None,
    status: Optional[NotificationStatus] = None,
    notification_type: Optional[str] = None
) -> int:
    """
    Count notifications with filtering options
    
    Args:
        recipient_id: Filter by recipient ID
        status: Filter by status
        notification_type: Filter by notification type
        
    Returns:
        Number of matching notifications
    """
    # Build query
    query = {}
    
    if recipient_id:
        query["recipient_id"] = recipient_id
        
    if status:
        query["status"] = status
        
    if notification_type:
        query["notification_type"] = notification_type
        
    # Execute count
    return notification_collection.count_documents(query)