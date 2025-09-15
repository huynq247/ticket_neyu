from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId

from app.api.deps import security, get_current_user
from app.models.notification import create_notification, get_notification, update_notification, list_notifications, count_notifications
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationList, Notification, NotificationType
from app.tasks.email import send_email_notification
from app.tasks.telegram import send_telegram_notification

router = APIRouter()


@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification_endpoint(
    notification_data: NotificationCreate,
    current_user = Depends(get_current_user)
):
    """
    Create and send a new notification
    """
    # Create notification in database
    notification = create_notification(notification_data)
    
    # Convert ObjectId to string
    notification["_id"] = str(notification["_id"])
    
    # Send notification based on type
    if notification_data.notification_type == NotificationType.EMAIL:
        send_email_notification.delay(notification["_id"])
    elif notification_data.notification_type == NotificationType.TELEGRAM:
        send_telegram_notification.delay(notification["_id"])
        
    return notification


@router.get("/{notification_id}", response_model=Notification)
async def get_notification_endpoint(
    notification_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Get notification by ID
    """
    notification = get_notification(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Convert ObjectId to string
    notification["_id"] = str(notification["_id"])
    
    return notification


@router.get("/", response_model=NotificationList)
async def list_notifications_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    recipient_id: Optional[str] = Query(None),
    notification_type: Optional[NotificationType] = Query(None),
    status: Optional[str] = Query(None),
    current_user = Depends(get_current_user)
):
    """
    List notifications with filtering options
    """
    # Get notifications from database
    notifications = list_notifications(skip, limit, recipient_id, status, notification_type)
    total = count_notifications(recipient_id, status, notification_type)
    
    # Convert ObjectId to string
    for notification in notifications:
        notification["_id"] = str(notification["_id"])
    
    return NotificationList(total=total, notifications=notifications)


@router.post("/resend/{notification_id}", response_model=Notification)
async def resend_notification_endpoint(
    notification_id: str = Path(...),
    current_user = Depends(get_current_user)
):
    """
    Resend a failed notification
    """
    notification = get_notification(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Only failed notifications can be resent
    if notification["status"] != "failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only failed notifications can be resent"
        )
    
    # Update notification status to pending
    updated = update_notification(
        notification_id=notification_id,
        update_data=NotificationUpdate(status="pending")
    )
    
    # Send notification based on type
    if notification["notification_type"] == NotificationType.EMAIL:
        send_email_notification.delay(notification_id)
    elif notification["notification_type"] == NotificationType.TELEGRAM:
        send_telegram_notification.delay(notification_id)
    
    # Convert ObjectId to string
    updated["_id"] = str(updated["_id"])
    
    return updated