import asyncio
import httpx
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, cast, Date
import json

from app.core.config import settings
from app.db.database import get_db
from app.models.sql_models import (
    FactTicket, DimDate, DimUser, DimCategory, 
    DimPriority, DimStatus, FactUserActivity, ETLLog
)
from app.api.deps import get_service_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """
    ETL Pipeline for data extraction, transformation and loading
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.service_token = get_service_token()
    
    async def extract_ticket_data(self, days: int = 1) -> List[Dict[str, Any]]:
        """
        Extract ticket data from Ticket Service
        """
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.service_token}"}
                response = await client.get(
                    f"{settings.TICKET_SERVICE_URL}/api/tickets?from_date={from_date}&limit={settings.ETL_BATCH_SIZE}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("tickets", [])
                else:
                    logger.error(f"Failed to extract ticket data: {response.status_code} - {response.text}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error extracting ticket data: {str(e)}")
            return []
    
    async def extract_user_data(self) -> List[Dict[str, Any]]:
        """
        Extract user data from User Service
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.service_token}"}
                response = await client.get(
                    f"{settings.USER_SERVICE_URL}/api/users?limit={settings.ETL_BATCH_SIZE}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("users", [])
                else:
                    logger.error(f"Failed to extract user data: {response.status_code} - {response.text}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error extracting user data: {str(e)}")
            return []
    
    async def extract_category_data(self) -> List[Dict[str, Any]]:
        """
        Extract category data from Ticket Service
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.service_token}"}
                response = await client.get(
                    f"{settings.TICKET_SERVICE_URL}/api/categories",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("categories", [])
                else:
                    logger.error(f"Failed to extract category data: {response.status_code} - {response.text}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error extracting category data: {str(e)}")
            return []
    
    def get_or_create_date_dimension(self, date_value: datetime) -> DimDate:
        """
        Get or create a date dimension record
        """
        date_obj = date_value.date()
        
        # Check if date exists
        date_dim = self.db.query(DimDate).filter(
            func.date(DimDate.date) == date_obj
        ).first()
        
        if date_dim:
            return date_dim
        
        # Create new date dimension
        weekday = date_obj.weekday()
        month = date_obj.month
        
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        month_names = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        
        new_date = DimDate(
            date=date_value,
            day=date_obj.day,
            day_of_week=weekday,
            day_name=day_names[weekday],
            month=month,
            month_name=month_names[month-1],
            quarter=(month-1)//3 + 1,
            year=date_obj.year,
            is_weekend=weekday >= 5,  # 5=Saturday, 6=Sunday
            is_holiday=False  # We can add holiday detection logic later
        )
        
        self.db.add(new_date)
        self.db.commit()
        self.db.refresh(new_date)
        
        return new_date
    
    def get_or_create_user_dimension(self, user_data: Dict[str, Any]) -> DimUser:
        """
        Get or create a user dimension record
        """
        user_id = user_data.get("id")
        
        # Check if user exists
        user_dim = self.db.query(DimUser).filter(DimUser.user_id == user_id).first()
        
        if user_dim:
            # Update user data
            user_dim.username = user_data.get("username")
            user_dim.email = user_data.get("email")
            user_dim.full_name = user_data.get("full_name")
            user_dim.department = user_data.get("department")
            user_dim.role = user_data.get("role")
            user_dim.is_active = user_data.get("is_active", True)
            user_dim.last_login = user_data.get("last_login")
            user_dim.etl_updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(user_dim)
            return user_dim
        
        # Create new user dimension
        new_user = DimUser(
            user_id=user_id,
            username=user_data.get("username"),
            email=user_data.get("email"),
            full_name=user_data.get("full_name"),
            department=user_data.get("department"),
            role=user_data.get("role"),
            is_active=user_data.get("is_active", True),
            created_at=user_data.get("created_at"),
            last_login=user_data.get("last_login"),
            etl_updated_at=datetime.utcnow()
        )
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return new_user
    
    def get_or_create_category_dimension(self, category_data: Dict[str, Any]) -> DimCategory:
        """
        Get or create a category dimension record
        """
        category_id = category_data.get("id")
        
        # Check if category exists
        category_dim = self.db.query(DimCategory).filter(DimCategory.category_id == category_id).first()
        
        if category_dim:
            # Update category data
            category_dim.name = category_data.get("name")
            category_dim.description = category_data.get("description")
            category_dim.etl_updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(category_dim)
            return category_dim
        
        # Create new category dimension
        new_category = DimCategory(
            category_id=category_id,
            name=category_data.get("name"),
            description=category_data.get("description"),
            etl_updated_at=datetime.utcnow()
        )
        
        # Handle parent category if exists
        parent_id = category_data.get("parent_id")
        if parent_id:
            parent_category = self.db.query(DimCategory).filter(DimCategory.category_id == parent_id).first()
            if parent_category:
                new_category.parent_category_id = parent_category.id
        
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        
        return new_category
    
    def get_or_create_priority_dimension(self, priority_data: Dict[str, Any]) -> DimPriority:
        """
        Get or create a priority dimension record
        """
        priority_id = priority_data.get("id")
        
        # Check if priority exists
        priority_dim = self.db.query(DimPriority).filter(DimPriority.priority_id == priority_id).first()
        
        if priority_dim:
            # Update priority data
            priority_dim.name = priority_data.get("name")
            priority_dim.level = priority_data.get("level")
            priority_dim.sla_minutes = priority_data.get("sla_minutes")
            priority_dim.description = priority_data.get("description")
            priority_dim.etl_updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(priority_dim)
            return priority_dim
        
        # Create new priority dimension
        new_priority = DimPriority(
            priority_id=priority_id,
            name=priority_data.get("name"),
            level=priority_data.get("level"),
            sla_minutes=priority_data.get("sla_minutes"),
            description=priority_data.get("description"),
            etl_updated_at=datetime.utcnow()
        )
        
        self.db.add(new_priority)
        self.db.commit()
        self.db.refresh(new_priority)
        
        return new_priority
    
    def get_or_create_status_dimension(self, status_data: Dict[str, Any]) -> DimStatus:
        """
        Get or create a status dimension record
        """
        status_id = status_data.get("id")
        
        # Check if status exists
        status_dim = self.db.query(DimStatus).filter(DimStatus.status_id == status_id).first()
        
        if status_dim:
            # Update status data
            status_dim.name = status_data.get("name")
            status_dim.description = status_data.get("description")
            status_dim.is_open = status_data.get("is_open", True)
            status_dim.is_closed = status_data.get("is_closed", False)
            status_dim.etl_updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(status_dim)
            return status_dim
        
        # Create new status dimension
        new_status = DimStatus(
            status_id=status_id,
            name=status_data.get("name"),
            description=status_data.get("description"),
            is_open=status_data.get("is_open", True),
            is_closed=status_data.get("is_closed", False),
            etl_updated_at=datetime.utcnow()
        )
        
        self.db.add(new_status)
        self.db.commit()
        self.db.refresh(new_status)
        
        return new_status
    
    def process_ticket_data(self, ticket_data: List[Dict[str, Any]]) -> None:
        """
        Process ticket data and load into data warehouse
        """
        for ticket in ticket_data:
            try:
                ticket_id = ticket.get("id")
                
                # Check if ticket exists
                existing_ticket = self.db.query(FactTicket).filter(FactTicket.ticket_id == ticket_id).first()
                
                # Get dimension records
                created_at = datetime.fromisoformat(ticket.get("created_at").replace('Z', '+00:00')) if ticket.get("created_at") else None
                updated_at = datetime.fromisoformat(ticket.get("updated_at").replace('Z', '+00:00')) if ticket.get("updated_at") else None
                resolved_at = datetime.fromisoformat(ticket.get("resolved_at").replace('Z', '+00:00')) if ticket.get("resolved_at") else None
                
                created_date_id = self.get_or_create_date_dimension(created_at).id if created_at else None
                updated_date_id = self.get_or_create_date_dimension(updated_at).id if updated_at else None
                resolved_date_id = self.get_or_create_date_dimension(resolved_at).id if resolved_at else None
                
                # Calculate metrics
                response_time_minutes = None
                resolution_time_minutes = None
                
                first_response_at = datetime.fromisoformat(ticket.get("first_response_at").replace('Z', '+00:00')) if ticket.get("first_response_at") else None
                
                if first_response_at and created_at:
                    response_time_minutes = (first_response_at - created_at).total_seconds() / 60
                
                if resolved_at and created_at:
                    resolution_time_minutes = (resolved_at - created_at).total_seconds() / 60
                
                if existing_ticket:
                    # Update existing ticket
                    existing_ticket.updated_date_id = updated_date_id
                    existing_ticket.resolved_date_id = resolved_date_id
                    existing_ticket.response_time_minutes = response_time_minutes
                    existing_ticket.resolution_time_minutes = resolution_time_minutes
                    existing_ticket.reopened_count = ticket.get("reopened_count", 0)
                    existing_ticket.comment_count = ticket.get("comment_count", 0)
                    existing_ticket.attachment_count = ticket.get("attachment_count", 0)
                    existing_ticket.etl_updated_at = datetime.utcnow()
                    
                    self.db.commit()
                    
                else:
                    # Create new ticket record
                    # Get foreign key references first
                    user_data = {"id": ticket.get("created_by")} if ticket.get("created_by") else None
                    assigned_to_data = {"id": ticket.get("assigned_to")} if ticket.get("assigned_to") else None
                    category_data = {"id": ticket.get("category_id")} if ticket.get("category_id") else None
                    priority_data = {"id": ticket.get("priority_id")} if ticket.get("priority_id") else None
                    status_data = {"id": ticket.get("status_id")} if ticket.get("status_id") else None
                    
                    user_id = self.get_or_create_user_dimension(user_data).id if user_data else None
                    assigned_to_id = self.get_or_create_user_dimension(assigned_to_data).id if assigned_to_data else None
                    category_id = self.get_or_create_category_dimension(category_data).id if category_data else None
                    priority_id = self.get_or_create_priority_dimension(priority_data).id if priority_data else None
                    status_id = self.get_or_create_status_dimension(status_data).id if status_data else None
                    
                    new_ticket = FactTicket(
                        ticket_id=ticket_id,
                        created_date_id=created_date_id,
                        updated_date_id=updated_date_id,
                        resolved_date_id=resolved_date_id,
                        user_id=user_id,
                        assigned_to_id=assigned_to_id,
                        category_id=category_id,
                        priority_id=priority_id,
                        status_id=status_id,
                        response_time_minutes=response_time_minutes,
                        resolution_time_minutes=resolution_time_minutes,
                        reopened_count=ticket.get("reopened_count", 0),
                        comment_count=ticket.get("comment_count", 0),
                        attachment_count=ticket.get("attachment_count", 0),
                        title=ticket.get("title"),
                        description=ticket.get("description"),
                        etl_updated_at=datetime.utcnow()
                    )
                    
                    self.db.add(new_ticket)
                    self.db.commit()
                
            except Exception as e:
                logger.error(f"Error processing ticket {ticket.get('id')}: {str(e)}")
                self.db.rollback()
    
    def process_user_activity(self, date: datetime = None) -> None:
        """
        Process user activity data and load into data warehouse
        """
        if not date:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        date_dim = self.get_or_create_date_dimension(date)
        
        # Get all users
        users = self.db.query(DimUser).all()
        
        for user in users:
            try:
                # Check if activity exists for this user and date
                existing_activity = self.db.query(FactUserActivity).filter(
                    FactUserActivity.date_id == date_dim.id,
                    FactUserActivity.user_id == user.id
                ).first()
                
                if existing_activity:
                    # We'll skip updating existing activity for simplicity
                    continue
                
                # Calculate activity metrics for this user on this date
                tickets_created = self.db.query(FactTicket).filter(
                    FactTicket.user_id == user.id,
                    FactTicket.created_date_id == date_dim.id
                ).count()
                
                tickets_closed = self.db.query(FactTicket).join(
                    DimStatus, FactTicket.status_id == DimStatus.id
                ).filter(
                    FactTicket.assigned_to_id == user.id,
                    FactTicket.resolved_date_id == date_dim.id,
                    DimStatus.is_closed == True
                ).count()
                
                # Create new activity record
                new_activity = FactUserActivity(
                    date_id=date_dim.id,
                    user_id=user.id,
                    tickets_created=tickets_created,
                    tickets_closed=tickets_closed,
                    tickets_reopened=0,  # We'd need more data to calculate this
                    comments_created=0,  # We'd need comment data to calculate this
                    logins=0,  # We'd need login data to calculate this
                    active_time_minutes=0,  # We'd need activity tracking to calculate this
                    etl_updated_at=datetime.utcnow()
                )
                
                self.db.add(new_activity)
                self.db.commit()
                
            except Exception as e:
                logger.error(f"Error processing user activity for user {user.user_id}: {str(e)}")
                self.db.rollback()
    
    async def run_etl_pipeline(self, days: int = 1) -> None:
        """
        Run the complete ETL pipeline
        """
        # Log ETL start
        etl_log = ETLLog(
            process_name="full_etl_pipeline",
            status="running"
        )
        self.db.add(etl_log)
        self.db.commit()
        
        try:
            # Extract data
            ticket_data = await self.extract_ticket_data(days)
            user_data = await self.extract_user_data()
            category_data = await self.extract_category_data()
            
            # Process dimensions first
            for user in user_data:
                self.get_or_create_user_dimension(user)
            
            for category in category_data:
                self.get_or_create_category_dimension(category)
            
            # Process facts
            self.process_ticket_data(ticket_data)
            
            # Process user activity for yesterday and today
            yesterday = datetime.now() - timedelta(days=1)
            yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            self.process_user_activity(yesterday)
            self.process_user_activity(today)
            
            # Update ETL log
            etl_log.end_time = datetime.utcnow()
            etl_log.status = "success"
            etl_log.records_processed = len(ticket_data) + len(user_data) + len(category_data)
            self.db.commit()
            
            logger.info(f"ETL pipeline completed successfully. Processed {etl_log.records_processed} records.")
            
        except Exception as e:
            # Log error and rollback
            logger.error(f"Error in ETL pipeline: {str(e)}")
            
            etl_log.end_time = datetime.utcnow()
            etl_log.status = "failed"
            etl_log.error_message = str(e)
            self.db.commit()


async def run_daily_etl():
    """
    Run daily ETL job
    """
    logger.info("Starting daily ETL job")
    
    db = next(get_db())
    pipeline = ETLPipeline(db)
    
    try:
        await pipeline.run_etl_pipeline(days=1)
        logger.info("Daily ETL job completed")
    except Exception as e:
        logger.error(f"Error in daily ETL job: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    # This can be used to run the ETL manually
    asyncio.run(run_daily_etl())