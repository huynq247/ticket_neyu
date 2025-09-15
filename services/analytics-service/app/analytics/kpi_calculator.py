from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case
from datetime import datetime, timedelta
from typing import List, Dict, Any

from app.schemas.analytics import KPIData
from app.models.sql_models import (
    FactTicket, DimDate, DimUser, DimCategory, 
    DimPriority, DimStatus, FactUserActivity
)

def calculate_kpis(
    db: Session, 
    start_date: datetime, 
    end_date: datetime
) -> List[KPIData]:
    """
    Calculate KPIs for the dashboard
    """
    kpis = []
    
    # Calculate previous period for comparison
    period_length = (end_date - start_date).days
    prev_end_date = start_date - timedelta(days=1)
    prev_start_date = prev_end_date - timedelta(days=period_length)
    
    # Calculate ticket resolution rate
    resolution_rate = calculate_resolution_rate(db, start_date, end_date)
    prev_resolution_rate = calculate_resolution_rate(db, prev_start_date, prev_end_date)
    
    if resolution_rate is not None and prev_resolution_rate is not None:
        change_percentage = ((resolution_rate - prev_resolution_rate) / prev_resolution_rate) * 100 if prev_resolution_rate > 0 else None
        
        kpis.append(KPIData(
            name="Resolution Rate",
            value=resolution_rate,
            target=0.9,  # 90% target resolution rate
            previous_value=prev_resolution_rate,
            change_percentage=change_percentage,
            trend=get_resolution_rate_trend(db, start_date, end_date)
        ))
    
    # Calculate average response time
    avg_response_time = calculate_avg_response_time(db, start_date, end_date)
    prev_avg_response_time = calculate_avg_response_time(db, prev_start_date, prev_end_date)
    
    if avg_response_time is not None and prev_avg_response_time is not None:
        # For response time, lower is better, so we invert the change percentage
        change_percentage = ((prev_avg_response_time - avg_response_time) / prev_avg_response_time) * 100 if prev_avg_response_time > 0 else None
        
        kpis.append(KPIData(
            name="Avg Response Time (minutes)",
            value=avg_response_time,
            target=60,  # 1 hour target response time
            previous_value=prev_avg_response_time,
            change_percentage=change_percentage,
            trend=get_response_time_trend(db, start_date, end_date)
        ))
    
    # Calculate average resolution time
    avg_resolution_time = calculate_avg_resolution_time(db, start_date, end_date)
    prev_avg_resolution_time = calculate_avg_resolution_time(db, prev_start_date, prev_end_date)
    
    if avg_resolution_time is not None and prev_avg_resolution_time is not None:
        # For resolution time, lower is better, so we invert the change percentage
        change_percentage = ((prev_avg_resolution_time - avg_resolution_time) / prev_avg_resolution_time) * 100 if prev_avg_resolution_time > 0 else None
        
        kpis.append(KPIData(
            name="Avg Resolution Time (minutes)",
            value=avg_resolution_time,
            target=1440,  # 24 hours target resolution time
            previous_value=prev_avg_resolution_time,
            change_percentage=change_percentage,
            trend=get_resolution_time_trend(db, start_date, end_date)
        ))
    
    # Calculate customer satisfaction
    # This would typically come from a feedback system, but we'll simulate it
    satisfaction_rate = calculate_satisfaction_rate(db, start_date, end_date)
    prev_satisfaction_rate = calculate_satisfaction_rate(db, prev_start_date, prev_end_date)
    
    if satisfaction_rate is not None and prev_satisfaction_rate is not None:
        change_percentage = ((satisfaction_rate - prev_satisfaction_rate) / prev_satisfaction_rate) * 100 if prev_satisfaction_rate > 0 else None
        
        kpis.append(KPIData(
            name="Customer Satisfaction",
            value=satisfaction_rate,
            target=0.9,  # 90% target satisfaction rate
            previous_value=prev_satisfaction_rate,
            change_percentage=change_percentage,
            trend=get_satisfaction_trend(db, start_date, end_date)
        ))
    
    return kpis

def calculate_resolution_rate(
    db: Session, 
    start_date: datetime, 
    end_date: datetime
) -> float:
    """
    Calculate the ticket resolution rate
    (Resolved tickets / Total tickets)
    """
    # Get total tickets created in the period
    total_tickets = db.query(FactTicket)\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .filter(DimDate.date >= start_date, DimDate.date <= end_date)\
        .count()
    
    if total_tickets == 0:
        return None
    
    # Get resolved tickets in the period
    resolved_tickets = db.query(FactTicket)\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .join(DimStatus, FactTicket.status_id == DimStatus.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            DimStatus.is_closed == True
        )\
        .count()
    
    # Calculate resolution rate
    return resolved_tickets / total_tickets

def get_resolution_rate_trend(
    db: Session, 
    start_date: datetime, 
    end_date: datetime,
    points: int = 7
) -> List[float]:
    """
    Get trend data for resolution rate
    """
    # Calculate the time step based on the date range and number of points
    period_length = (end_date - start_date).days
    step = max(1, period_length // points)
    
    trend = []
    for i in range(points):
        point_start = start_date + timedelta(days=i * step)
        point_end = min(end_date, point_start + timedelta(days=step - 1))
        
        rate = calculate_resolution_rate(db, point_start, point_end)
        if rate is not None:
            trend.append(rate)
        else:
            trend.append(0)  # Fallback if no data
    
    return trend

def calculate_avg_response_time(
    db: Session, 
    start_date: datetime, 
    end_date: datetime
) -> float:
    """
    Calculate the average response time in minutes
    """
    avg_time = db.query(
        func.avg(FactTicket.response_time_minutes)
    )\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            FactTicket.response_time_minutes.isnot(None)
        )\
        .scalar()
    
    return float(avg_time) if avg_time is not None else None

def get_response_time_trend(
    db: Session, 
    start_date: datetime, 
    end_date: datetime,
    points: int = 7
) -> List[float]:
    """
    Get trend data for average response time
    """
    # Calculate the time step based on the date range and number of points
    period_length = (end_date - start_date).days
    step = max(1, period_length // points)
    
    trend = []
    for i in range(points):
        point_start = start_date + timedelta(days=i * step)
        point_end = min(end_date, point_start + timedelta(days=step - 1))
        
        avg_time = calculate_avg_response_time(db, point_start, point_end)
        if avg_time is not None:
            trend.append(avg_time)
        else:
            # If no data, use the previous point or 0
            trend.append(trend[-1] if trend else 0)
    
    return trend

def calculate_avg_resolution_time(
    db: Session, 
    start_date: datetime, 
    end_date: datetime
) -> float:
    """
    Calculate the average resolution time in minutes
    """
    avg_time = db.query(
        func.avg(FactTicket.resolution_time_minutes)
    )\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            FactTicket.resolution_time_minutes.isnot(None)
        )\
        .scalar()
    
    return float(avg_time) if avg_time is not None else None

def get_resolution_time_trend(
    db: Session, 
    start_date: datetime, 
    end_date: datetime,
    points: int = 7
) -> List[float]:
    """
    Get trend data for average resolution time
    """
    # Calculate the time step based on the date range and number of points
    period_length = (end_date - start_date).days
    step = max(1, period_length // points)
    
    trend = []
    for i in range(points):
        point_start = start_date + timedelta(days=i * step)
        point_end = min(end_date, point_start + timedelta(days=step - 1))
        
        avg_time = calculate_avg_resolution_time(db, point_start, point_end)
        if avg_time is not None:
            trend.append(avg_time)
        else:
            # If no data, use the previous point or 0
            trend.append(trend[-1] if trend else 0)
    
    return trend

def calculate_satisfaction_rate(
    db: Session, 
    start_date: datetime, 
    end_date: datetime
) -> float:
    """
    Calculate the customer satisfaction rate
    This is a simulated metric since we don't have actual satisfaction data
    """
    # In a real system, this would come from feedback data
    # Here, we'll simulate it based on resolution time and reopened tickets
    
    # Get tickets with resolution time
    tickets = db.query(
        FactTicket.resolution_time_minutes,
        FactTicket.reopened_count
    )\
        .join(DimDate, FactTicket.created_date_id == DimDate.id)\
        .filter(
            DimDate.date >= start_date,
            DimDate.date <= end_date,
            FactTicket.resolution_time_minutes.isnot(None)
        )\
        .all()
    
    if not tickets:
        return None
    
    # Simulate satisfaction based on resolution time and reopens
    # The formula is arbitrary for demonstration
    total_satisfaction = 0
    for resolution_time, reopened_count in tickets:
        # Base satisfaction starts at 1.0 (100%)
        satisfaction = 1.0
        
        # Reduce satisfaction based on resolution time
        if resolution_time > 1440:  # More than 24 hours
            satisfaction -= 0.3
        elif resolution_time > 480:  # More than 8 hours
            satisfaction -= 0.1
        elif resolution_time > 120:  # More than 2 hours
            satisfaction -= 0.05
        
        # Reduce satisfaction based on reopens
        satisfaction -= reopened_count * 0.2
        
        # Ensure satisfaction is between 0 and 1
        satisfaction = max(0, min(1, satisfaction))
        
        total_satisfaction += satisfaction
    
    return total_satisfaction / len(tickets)

def get_satisfaction_trend(
    db: Session, 
    start_date: datetime, 
    end_date: datetime,
    points: int = 7
) -> List[float]:
    """
    Get trend data for customer satisfaction
    """
    # Calculate the time step based on the date range and number of points
    period_length = (end_date - start_date).days
    step = max(1, period_length // points)
    
    trend = []
    for i in range(points):
        point_start = start_date + timedelta(days=i * step)
        point_end = min(end_date, point_start + timedelta(days=step - 1))
        
        satisfaction = calculate_satisfaction_rate(db, point_start, point_end)
        if satisfaction is not None:
            trend.append(satisfaction)
        else:
            # If no data, use the previous point or 0.75 (default)
            trend.append(trend[-1] if trend else 0.75)
    
    return trend