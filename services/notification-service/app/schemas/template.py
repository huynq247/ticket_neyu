from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class TemplateType(str, Enum):
    EMAIL = "email"
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"


class TemplateBase(BaseModel):
    """Base Template schema with common attributes"""
    name: str
    type: TemplateType
    subject: Optional[str] = None
    content: str
    description: Optional[str] = None


class TemplateCreate(TemplateBase):
    """Schema for template creation"""
    pass


class TemplateUpdate(BaseModel):
    """Schema for template update"""
    subject: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None


class TemplateInDB(TemplateBase):
    """Schema for template in database"""
    id: str = Field(..., alias="_id")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True


class Template(TemplateInDB):
    """Schema for template response"""
    pass


class TemplateList(BaseModel):
    """Schema for list of templates"""
    total: int
    templates: List[Template]