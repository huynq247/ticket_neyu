from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, Any, List

from app.db.database import Base

class FactTicket(Base):
    """
    Fact table for tickets - contains metrics and foreign keys to dimensions
    """
    __tablename__ = "fact_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True, nullable=False)
    
    # Foreign keys to dimension tables
    created_date_id = Column(Integer, ForeignKey("dim_dates.id"))
    updated_date_id = Column(Integer, ForeignKey("dim_dates.id"))
    resolved_date_id = Column(Integer, ForeignKey("dim_dates.id"))
    user_id = Column(Integer, ForeignKey("dim_users.id"))
    assigned_to_id = Column(Integer, ForeignKey("dim_users.id"))
    category_id = Column(Integer, ForeignKey("dim_categories.id"))
    priority_id = Column(Integer, ForeignKey("dim_priorities.id"))
    status_id = Column(Integer, ForeignKey("dim_statuses.id"))
    
    # Metrics
    response_time_minutes = Column(Float)
    resolution_time_minutes = Column(Float)
    reopened_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    attachment_count = Column(Integer, default=0)
    
    # Ticket details
    title = Column(String(255))
    description = Column(Text)
    
    # ETL tracking
    etl_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    created_date = relationship("DimDate", foreign_keys=[created_date_id])
    updated_date = relationship("DimDate", foreign_keys=[updated_date_id])
    resolved_date = relationship("DimDate", foreign_keys=[resolved_date_id])
    creator = relationship("DimUser", foreign_keys=[user_id])
    assignee = relationship("DimUser", foreign_keys=[assigned_to_id])
    category = relationship("DimCategory")
    priority = relationship("DimPriority")
    status = relationship("DimStatus")


class DimDate(Base):
    """
    Date dimension table
    """
    __tablename__ = "dim_dates"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, index=True)
    day = Column(Integer)
    day_of_week = Column(Integer)
    day_name = Column(String(10))
    month = Column(Integer)
    month_name = Column(String(10))
    quarter = Column(Integer)
    year = Column(Integer)
    is_weekend = Column(Boolean)
    is_holiday = Column(Boolean, default=False)
    holiday_name = Column(String(50), nullable=True)


class DimUser(Base):
    """
    User dimension table
    """
    __tablename__ = "dim_users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String(100))
    email = Column(String(100))
    full_name = Column(String(100))
    department = Column(String(100))
    role = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    last_login = Column(DateTime)
    etl_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DimCategory(Base):
    """
    Category dimension table
    """
    __tablename__ = "dim_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(100))
    description = Column(Text)
    parent_category_id = Column(Integer, ForeignKey("dim_categories.id"), nullable=True)
    etl_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Self-referential relationship
    parent_category = relationship("DimCategory", remote_side=[id])


class DimPriority(Base):
    """
    Priority dimension table
    """
    __tablename__ = "dim_priorities"
    
    id = Column(Integer, primary_key=True, index=True)
    priority_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(50))
    level = Column(Integer)
    sla_minutes = Column(Integer)
    description = Column(Text)
    etl_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DimStatus(Base):
    """
    Status dimension table
    """
    __tablename__ = "dim_statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    status_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(50))
    description = Column(Text)
    is_open = Column(Boolean, default=True)
    is_closed = Column(Boolean, default=False)
    etl_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FactUserActivity(Base):
    """
    Fact table for user activity
    """
    __tablename__ = "fact_user_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys to dimension tables
    date_id = Column(Integer, ForeignKey("dim_dates.id"))
    user_id = Column(Integer, ForeignKey("dim_users.id"))
    
    # Activity metrics
    tickets_created = Column(Integer, default=0)
    tickets_closed = Column(Integer, default=0)
    tickets_reopened = Column(Integer, default=0)
    comments_created = Column(Integer, default=0)
    logins = Column(Integer, default=0)
    active_time_minutes = Column(Float, default=0)
    
    # ETL tracking
    etl_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    date = relationship("DimDate")
    user = relationship("DimUser")


class ETLLog(Base):
    """
    Log table for ETL processes
    """
    __tablename__ = "etl_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    process_name = Column(String(100))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(20))  # 'running', 'success', 'failed'
    records_processed = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)