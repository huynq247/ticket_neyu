from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.core.database import scheduled_report_collection
from app.schemas.report import ScheduledReportCreate, ScheduledReportUpdate, ScheduleFrequency


def create_scheduled_report(report_data: ScheduledReportCreate, user_id: str) -> Dict[str, Any]:
    """
    Create a new scheduled report
    """
    # Convert to dict
    report_dict = report_data.model_dump()
    
    # Add metadata
    now = datetime.utcnow()
    report_dict["created_by"] = user_id
    report_dict["created_at"] = now
    report_dict["updated_at"] = now
    report_dict["active"] = True
    
    # Calculate next run time
    next_run = calculate_next_run(
        frequency=report_data.frequency,
        day_of_week=report_data.day_of_week,
        day_of_month=report_data.day_of_month,
        hour=report_data.hour,
        minute=report_data.minute
    )
    report_dict["next_run"] = next_run
    
    # Insert into database
    result = scheduled_report_collection.insert_one(report_dict)
    
    # Get created document
    created_report = scheduled_report_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string
    if created_report:
        created_report["id"] = str(created_report.pop("_id"))
    
    return created_report


def get_scheduled_report(report_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a scheduled report by ID
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(report_id)
    except:
        return None
    
    # Find report
    report = scheduled_report_collection.find_one({"_id": object_id})
    
    # Convert ObjectId to string
    if report:
        report["id"] = str(report.pop("_id"))
    
    return report


def update_scheduled_report(report_id: str, report_data: ScheduledReportUpdate) -> Optional[Dict[str, Any]]:
    """
    Update a scheduled report
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(report_id)
    except:
        return None
    
    # Get report to update
    report = scheduled_report_collection.find_one({"_id": object_id})
    if not report:
        return None
    
    # Convert to dict and remove None values
    update_data = {k: v for k, v in report_data.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        return get_scheduled_report(report_id)
    
    # Check if schedule parameters are updated
    schedule_updated = any(
        param in update_data for param in 
        ["frequency", "day_of_week", "day_of_month", "hour", "minute"]
    )
    
    if schedule_updated:
        # Get current or updated values
        frequency = update_data.get("frequency", report["frequency"])
        day_of_week = update_data.get("day_of_week", report.get("day_of_week"))
        day_of_month = update_data.get("day_of_month", report.get("day_of_month"))
        hour = update_data.get("hour", report["hour"])
        minute = update_data.get("minute", report["minute"])
        
        # Calculate next run time
        next_run = calculate_next_run(
            frequency=frequency,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            hour=hour,
            minute=minute
        )
        update_data["next_run"] = next_run
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update report
    scheduled_report_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )
    
    # Get updated report
    return get_scheduled_report(report_id)


def list_scheduled_reports(
    user_id: str,
    skip: int = 0,
    limit: int = 20,
    active_only: bool = False
) -> List[Dict[str, Any]]:
    """
    List scheduled reports for a user
    """
    # Build query
    query = {"created_by": user_id}
    
    if active_only:
        query["active"] = True
    
    # Execute query
    cursor = scheduled_report_collection.find(query).skip(skip).limit(limit).sort("next_run", 1)
    
    # Convert results
    reports = []
    for report in cursor:
        report["id"] = str(report.pop("_id"))
        reports.append(report)
    
    return reports


def count_scheduled_reports(
    user_id: str,
    active_only: bool = False
) -> int:
    """
    Count scheduled reports for a user
    """
    # Build query
    query = {"created_by": user_id}
    
    if active_only:
        query["active"] = True
    
    # Execute count
    return scheduled_report_collection.count_documents(query)


def delete_scheduled_report(report_id: str) -> bool:
    """
    Delete a scheduled report
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(report_id)
    except:
        return False
    
    # Delete report
    result = scheduled_report_collection.delete_one({"_id": object_id})
    
    return result.deleted_count > 0


def get_due_reports() -> List[Dict[str, Any]]:
    """
    Get reports that are due to run
    """
    now = datetime.utcnow()
    
    # Find reports due to run
    query = {
        "active": True,
        "next_run": {"$lte": now}
    }
    
    cursor = scheduled_report_collection.find(query)
    
    # Convert results
    reports = []
    for report in cursor:
        report["id"] = str(report.pop("_id"))
        reports.append(report)
    
    return reports


def update_report_after_run(report_id: str) -> Optional[Dict[str, Any]]:
    """
    Update a report after it has been run
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(report_id)
    except:
        return None
    
    # Get report
    report = scheduled_report_collection.find_one({"_id": object_id})
    if not report:
        return None
    
    # Calculate next run time
    next_run = calculate_next_run(
        frequency=report["frequency"],
        day_of_week=report.get("day_of_week"),
        day_of_month=report.get("day_of_month"),
        hour=report["hour"],
        minute=report["minute"]
    )
    
    now = datetime.utcnow()
    
    # Update report
    scheduled_report_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "last_run": now,
                "next_run": next_run,
                "updated_at": now
            }
        }
    )
    
    # Get updated report
    return get_scheduled_report(str(object_id))


def calculate_next_run(
    frequency: ScheduleFrequency,
    hour: int,
    minute: int,
    day_of_week: Optional[int] = None,
    day_of_month: Optional[int] = None
) -> datetime:
    """
    Calculate the next run time based on frequency and time
    """
    now = datetime.utcnow()
    
    # Start with today at specified hour and minute
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # If the time is in the past, start from tomorrow
    if next_run <= now:
        next_run += timedelta(days=1)
    
    if frequency == ScheduleFrequency.DAILY:
        # Already set for tomorrow if needed
        pass
        
    elif frequency == ScheduleFrequency.WEEKLY:
        if day_of_week is not None:
            # Adjust to the correct day of week (0 = Monday, 6 = Sunday)
            current_day = next_run.weekday()
            days_to_add = (day_of_week - current_day) % 7
            
            if days_to_add == 0 and next_run <= now:
                days_to_add = 7
                
            next_run += timedelta(days=days_to_add)
        
    elif frequency == ScheduleFrequency.MONTHLY:
        if day_of_month is not None:
            # Get the last day of the current month
            if next_run.month == 12:
                last_day = datetime(next_run.year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = datetime(next_run.year, next_run.month + 1, 1) - timedelta(days=1)
            
            # Ensure day_of_month is valid
            actual_day = min(day_of_month, last_day.day)
            
            # Set the day
            next_run = next_run.replace(day=actual_day)
            
            # If it's in the past, move to next month
            if next_run <= now:
                if next_run.month == 12:
                    next_run = next_run.replace(year=next_run.year + 1, month=1)
                else:
                    next_run = next_run.replace(month=next_run.month + 1)
                
                # Check the last day of the next month
                if next_run.month == 12:
                    last_day = datetime(next_run.year + 1, 1, 1) - timedelta(days=1)
                else:
                    last_day = datetime(next_run.year, next_run.month + 1, 1) - timedelta(days=1)
                
                actual_day = min(day_of_month, last_day.day)
                next_run = next_run.replace(day=actual_day)
    
    elif frequency == ScheduleFrequency.QUARTERLY:
        # Get the current quarter
        current_quarter = (now.month - 1) // 3
        
        # Set to the first month of the next quarter
        next_quarter_month = (current_quarter + 1) % 4 * 3 + 1
        next_quarter_year = now.year + (1 if next_quarter_month < now.month else 0)
        
        # Set the day (or default to 1st day of month)
        day = day_of_month or 1
        
        # Create the date for the next quarter
        next_run = datetime(next_quarter_year, next_quarter_month, day, hour, minute)
        
        # If it's in the past, move to the next quarter
        if next_run <= now:
            next_quarter_month = (current_quarter + 2) % 4 * 3 + 1
            next_quarter_year = now.year + (1 if next_quarter_month < now.month else 0)
            next_run = datetime(next_quarter_year, next_quarter_month, day, hour, minute)
    
    return next_run