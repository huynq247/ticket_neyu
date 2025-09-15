from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np

from app.api.deps import get_current_user, get_db_session
from app.schemas.analytics import (
    DashboardData, TicketMetrics, TimeSeriesData, 
    TimeSeriesDataPoint, KPIData, CategoryMetrics, 
    UserActivityMetrics, TimeGranularity
)
from app.models.sql_models import (
    FactTicket, DimDate, DimUser, DimCategory, 
    DimPriority, DimStatus, FactUserActivity
)
from app.analytics.kpi_calculator import calculate_kpis

router = APIRouter()


@router.get("/", response_model=DashboardData)
async def get_dashboard_data(
    start_date: Optional[date] = Query(None, description="Start date for dashboard data (inclusive)"),
    end_date: Optional[date] = Query(None, description="End date for dashboard data (inclusive)"),
    granularity: TimeGranularity = Query(TimeGranularity.DAY, description="Time granularity for time series data"),
    db: Session = Depends(get_db_session),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get main dashboard data with ticket metrics, time series, KPIs, and top performers
    """
    # Set default date range if not provided (last 30 days)
    if not end_date:
        end_date = datetime.now().date()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Convert to datetime for database query
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    # Get ticket metrics
    ticket_metrics = get_ticket_metrics(db, start_datetime, end_datetime)
    
    # Get time series data
    time_series = get_time_series_data(db, start_datetime, end_datetime, granularity)
    
    # Get KPIs
    kpis = calculate_kpis(db, start_datetime, end_datetime)
    
    # Get top categories
    top_categories = get_top_categories(db, start_datetime, end_datetime)
    
    # Get top users
    top_users = get_top_users(db, start_datetime, end_datetime)
    
    # Compile dashboard data
    dashboard_data = {
        "ticket_metrics": ticket_metrics,
        "time_series": time_series,
        "kpis": kpis,
        "top_categories": top_categories,
        "top_users": top_users
    }
    
    return dashboard_data


def get_ticket_metrics(
    db: Session, 
    start_date: datetime, 
    end_date: datetime
) -> TicketMetrics:
    """
    Calculate ticket metrics for the specified date range
    """
    # Get total tickets
    total_tickets = db.query(FactTicket)\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .filter(DimDate.date >= start_date, DimDate.date <= end_date)\
        .count()
    
    # Get open tickets
    open_tickets = db.query(FactTicket)\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .join(DimStatus, FactTicket.status_id == DimStatus.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            DimStatus.is_open == True
        )\
        .count()
    
    # Get closed tickets
    closed_tickets = db.query(FactTicket)\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .join(DimStatus, FactTicket.status_id == DimStatus.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            DimStatus.is_closed == True
        )\
        .count()
    
    # Get average response time
    avg_response_time = db.query(
        db.func.avg(FactTicket.response_time_minutes)
    )\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            FactTicket.response_time_minutes.isnot(None)
        )\
        .scalar()
    
    # Get average resolution time
    avg_resolution_time = db.query(
        db.func.avg(FactTicket.resolution_time_minutes)
    )\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            FactTicket.resolution_time_minutes.isnot(None)
        )\
        .scalar()
    
    # Get reopened tickets
    reopened_tickets = db.query(FactTicket)\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            FactTicket.reopened_count > 0
        )\
        .count()
    
    return TicketMetrics(
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        closed_tickets=closed_tickets,
        avg_response_time=float(avg_response_time) if avg_response_time else None,
        avg_resolution_time=float(avg_resolution_time) if avg_resolution_time else None,
        reopened_tickets=reopened_tickets
    )


def get_time_series_data(
    db: Session, 
    start_date: datetime, 
    end_date: datetime,
    granularity: TimeGranularity
) -> List[TimeSeriesData]:
    """
    Get time series data for tickets created, closed, and response times
    """
    time_series_list = []
    
    # Generate date range for the time series based on granularity
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        
        if granularity == TimeGranularity.DAY:
            current_date = current_date + timedelta(days=1)
        elif granularity == TimeGranularity.WEEK:
            current_date = current_date + timedelta(weeks=1)
        elif granularity == TimeGranularity.MONTH:
            # Add one month (approximately)
            month = current_date.month + 1
            year = current_date.year
            if month > 12:
                month = 1
                year += 1
            current_date = current_date.replace(year=year, month=month, day=1)
        elif granularity == TimeGranularity.QUARTER:
            # Add one quarter (3 months)
            month = current_date.month + 3
            year = current_date.year
            if month > 12:
                month = month - 12
                year += 1
            current_date = current_date.replace(year=year, month=month, day=1)
        elif granularity == TimeGranularity.YEAR:
            current_date = current_date.replace(year=current_date.year + 1)
    
    # Query data for tickets created over time
    tickets_created_data = []
    for date in date_range:
        # Adjust end date based on granularity
        if granularity == TimeGranularity.DAY:
            period_end = date.replace(hour=23, minute=59, second=59)
        elif granularity == TimeGranularity.WEEK:
            period_end = date + timedelta(days=6, hours=23, minutes=59, seconds=59)
        elif granularity == TimeGranularity.MONTH:
            # Last day of month
            next_month = date.replace(day=28) + timedelta(days=4)
            period_end = next_month - timedelta(days=next_month.day)
            period_end = period_end.replace(hour=23, minute=59, second=59)
        elif granularity == TimeGranularity.QUARTER:
            # Last day of quarter
            quarter_end_month = ((date.month - 1) // 3) * 3 + 3
            if quarter_end_month > 12:
                quarter_end_month = 12
            next_month = date.replace(month=quarter_end_month, day=28) + timedelta(days=4)
            period_end = next_month - timedelta(days=next_month.day)
            period_end = period_end.replace(hour=23, minute=59, second=59)
        elif granularity == TimeGranularity.YEAR:
            period_end = date.replace(month=12, day=31, hour=23, minute=59, second=59)
        
        # Skip if period_end is beyond the overall end_date
        if period_end > end_date:
            period_end = end_date
        
        # Count tickets created in this period
        ticket_count = db.query(FactTicket)\
            .join(DimDate, FactTicket.created_date_id == DimDate.id)\
            .filter(DimDate.date >= date, DimDate.date <= period_end)\
            .count()
        
        # Format date string based on granularity
        if granularity == TimeGranularity.DAY:
            date_str = date.strftime("%Y-%m-%d")
        elif granularity == TimeGranularity.WEEK:
            date_str = f"{date.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}"
        elif granularity == TimeGranularity.MONTH:
            date_str = date.strftime("%Y-%m")
        elif granularity == TimeGranularity.QUARTER:
            quarter = (date.month - 1) // 3 + 1
            date_str = f"{date.year} Q{quarter}"
        elif granularity == TimeGranularity.YEAR:
            date_str = str(date.year)
        
        tickets_created_data.append(
            TimeSeriesDataPoint(date=date_str, value=ticket_count)
        )
    
    # Add tickets created time series
    time_series_list.append(
        TimeSeriesData(
            metric="tickets_created",
            granularity=granularity,
            data=tickets_created_data
        )
    )
    
    # Query data for tickets closed over time
    tickets_closed_data = []
    for date in date_range:
        # Adjust end date based on granularity (similar to above)
        if granularity == TimeGranularity.DAY:
            period_end = date.replace(hour=23, minute=59, second=59)
        elif granularity == TimeGranularity.WEEK:
            period_end = date + timedelta(days=6, hours=23, minutes=59, seconds=59)
        elif granularity == TimeGranularity.MONTH:
            next_month = date.replace(day=28) + timedelta(days=4)
            period_end = next_month - timedelta(days=next_month.day)
            period_end = period_end.replace(hour=23, minute=59, second=59)
        elif granularity == TimeGranularity.QUARTER:
            quarter_end_month = ((date.month - 1) // 3) * 3 + 3
            if quarter_end_month > 12:
                quarter_end_month = 12
            next_month = date.replace(month=quarter_end_month, day=28) + timedelta(days=4)
            period_end = next_month - timedelta(days=next_month.day)
            period_end = period_end.replace(hour=23, minute=59, second=59)
        elif granularity == TimeGranularity.YEAR:
            period_end = date.replace(month=12, day=31, hour=23, minute=59, second=59)
        
        # Skip if period_end is beyond the overall end_date
        if period_end > end_date:
            period_end = end_date
        
        # Count tickets closed in this period
        ticket_count = db.query(FactTicket)\
            .join(DimDate, FactTicket.resolved_date_id == DimDate.id)\
            .join(DimStatus, FactTicket.status_id == DimStatus.id)\
            .filter(
                DimDate.date >= date,
                DimDate.date <= period_end,
                DimStatus.is_closed == True
            )\
            .count()
        
        # Format date string (same as above)
        if granularity == TimeGranularity.DAY:
            date_str = date.strftime("%Y-%m-%d")
        elif granularity == TimeGranularity.WEEK:
            date_str = f"{date.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}"
        elif granularity == TimeGranularity.MONTH:
            date_str = date.strftime("%Y-%m")
        elif granularity == TimeGranularity.QUARTER:
            quarter = (date.month - 1) // 3 + 1
            date_str = f"{date.year} Q{quarter}"
        elif granularity == TimeGranularity.YEAR:
            date_str = str(date.year)
        
        tickets_closed_data.append(
            TimeSeriesDataPoint(date=date_str, value=ticket_count)
        )
    
    # Add tickets closed time series
    time_series_list.append(
        TimeSeriesData(
            metric="tickets_closed",
            granularity=granularity,
            data=tickets_closed_data
        )
    )
    
    return time_series_list


def get_top_categories(
    db: Session, 
    start_date: datetime, 
    end_date: datetime,
    limit: int = 5
) -> List[CategoryMetrics]:
    """
    Get top categories by ticket count
    """
    # Query for top categories
    category_data = db.query(
        DimCategory,
        db.func.count(FactTicket.id).label("ticket_count"),
        db.func.avg(FactTicket.resolution_time_minutes).label("avg_resolution_time"),
        db.func.sum(db.case([(DimStatus.is_open == True, 1)], else_=0)).label("open_tickets"),
        db.func.sum(db.case([(DimStatus.is_closed == True, 1)], else_=0)).label("closed_tickets")
    )\
        .join(FactTicket, DimCategory.id == FactTicket.category_id)\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .join(DimStatus, FactTicket.status_id == DimStatus.id)\
        .filter(DimDate.date >= start_date, DimDate.date <= end_date)\
        .group_by(DimCategory.id)\
        .order_by(db.func.count(FactTicket.id).desc())\
        .limit(limit)\
        .all()
    
    # Convert to CategoryMetrics objects
    top_categories = []
    for category, ticket_count, avg_resolution_time, open_tickets, closed_tickets in category_data:
        top_categories.append(
            CategoryMetrics(
                category_id=category.category_id,
                name=category.name,
                ticket_count=ticket_count,
                avg_resolution_time=float(avg_resolution_time) if avg_resolution_time else None,
                open_tickets=open_tickets,
                closed_tickets=closed_tickets
            )
        )
    
    return top_categories


def get_top_users(
    db: Session, 
    start_date: datetime, 
    end_date: datetime,
    limit: int = 5
) -> List[UserActivityMetrics]:
    """
    Get top users by activity
    """
    # Query for top users by tickets created
    user_data = db.query(
        DimUser,
        db.func.sum(FactUserActivity.tickets_created).label("tickets_created"),
        db.func.sum(FactUserActivity.tickets_closed).label("tickets_closed"),
        db.func.sum(FactUserActivity.comments_created).label("comments_created"),
        db.func.sum(FactUserActivity.active_time_minutes).label("active_time_minutes")
    )\
        .join(FactUserActivity, DimUser.id == FactUserActivity.user_id)\
        .join(DimDate, FactUserActivity.date_id == DimDate.id)\
        .filter(DimDate.date >= start_date, DimDate.date <= end_date)\
        .group_by(DimUser.id)\
        .order_by(db.func.sum(FactUserActivity.tickets_created).desc())\
        .limit(limit)\
        .all()
    
    # Convert to UserActivityMetrics objects
    top_users = []
    for user, tickets_created, tickets_closed, comments_created, active_time_minutes in user_data:
        top_users.append(
            UserActivityMetrics(
                user_id=user.user_id,
                username=user.username,
                tickets_created=tickets_created,
                tickets_closed=tickets_closed,
                comments_created=comments_created,
                active_time_minutes=float(active_time_minutes) if active_time_minutes else 0
            )
        )
    
    return top_users