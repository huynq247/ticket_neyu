from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, Field


class NotificationType(str, Enum):
    EMAIL = "email"
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    SCHEDULED = "scheduled"


class NotificationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class NotificationBase(BaseModel):
    """Base Notification schema with common attributes"""
    notification_type: NotificationType
    recipient_id: str
    subject: Optional[str] = None
    template_name: str
    template_data: Dict[str, Any]
    priority: NotificationPriority = NotificationPriority.NORMAL
    scheduled_for: Optional[datetime] = None


class NotificationCreate(NotificationBase):
    """Schema for notification creation"""
    pass


class NotificationUpdate(BaseModel):
    """Schema for notification update"""
    status: Optional[NotificationStatus] = None
    error_message: Optional[str] = None
    sent_at: Optional[datetime] = None


class NotificationInDB(NotificationBase):
    """Schema for notification in database"""
    id: str = Field(..., alias="_id")
    status: NotificationStatus
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        populate_by_name = True


class Notification(NotificationInDB):
    """Schema for notification response"""
    pass


class NotificationList(BaseModel):
    """Schema for list of notifications"""
    total: int
    notifications: List[Notification]