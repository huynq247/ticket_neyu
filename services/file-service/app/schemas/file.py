from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class FileBase(BaseModel):
    """Base File schema with common attributes"""
    filename: str
    content_type: str
    size: int
    description: Optional[str] = None


class FileCreate(FileBase):
    """Schema for file creation"""
    owner_id: str
    ticket_id: Optional[str] = None
    tags: Optional[List[str]] = []


class FileUpdate(BaseModel):
    """Schema for file update"""
    filename: Optional[str] = None
    description: Optional[str] = None
    ticket_id: Optional[str] = None
    tags: Optional[List[str]] = None


class FileInDB(FileBase):
    """Schema for file in database"""
    id: str = Field(..., alias="_id")
    owner_id: str
    ticket_id: Optional[str] = None
    path: str
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []
    
    class Config:
        populate_by_name = True


class File(FileInDB):
    """Schema for file response"""
    download_url: str
    
    class Config:
        populate_by_name = True


class FileList(BaseModel):
    """Schema for list of files"""
    total: int
    files: List[File]