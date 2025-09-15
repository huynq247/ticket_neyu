from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CommentBase(BaseModel):
    content: str
    created_by: str  # User ID


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: str
    ticket_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TicketBase(BaseModel):
    title: str
    description: str
    category_id: str
    priority: TicketPriority = TicketPriority.MEDIUM
    requester_id: str  # User ID


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    assignee_id: Optional[str] = None  # User ID


class Ticket(TicketBase):
    id: str
    status: TicketStatus = TicketStatus.OPEN
    assignee_id: Optional[str] = None  # User ID
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[Comment] = []

    class Config:
        orm_mode = True


class TicketWithCategory(Ticket):
    category: Category

    class Config:
        orm_mode = True


class TicketListResponse(BaseModel):
    total: int
    items: List[Ticket]

    class Config:
        orm_mode = True