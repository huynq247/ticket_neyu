from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.core.database import report_collection
from app.schemas.report import ReportCreate, ReportType, ReportFormat, TimeRange


def create_report(report_data: ReportCreate, user_id: str) -> Dict[str, Any]:
    """
    Create a new report
    """
    # Convert to dict
    report_dict = report_data.model_dump()
    
    # Add metadata
    now = datetime.utcnow()
    report_dict["created_by"] = user_id
    report_dict["created_at"] = now
    report_dict["updated_at"] = now
    report_dict["status"] = "pending"
    
    # Insert into database
    result = report_collection.insert_one(report_dict)
    
    # Get created document
    created_report = report_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string
    if created_report:
        created_report["id"] = str(created_report.pop("_id"))
    
    return created_report


def get_report(report_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a report by ID
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(report_id)
    except:
        return None
    
    # Find report
    report = report_collection.find_one({"_id": object_id})
    
    # Convert ObjectId to string
    if report:
        report["id"] = str(report.pop("_id"))
    
    return report


def list_reports(
    user_id: str,
    skip: int = 0,
    limit: int = 20,
    report_type: Optional[ReportType] = None,
    time_range: Optional[TimeRange] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Dict[str, Any]]:
    """
    List reports with filtering
    """
    # Build query
    query = {"created_by": user_id}
    
    if report_type:
        query["params.report_type"] = report_type
        
    if time_range:
        query["params.time_range"] = time_range
        
    if start_date and end_date:
        query["created_at"] = {
            "$gte": start_date,
            "$lte": end_date
        }
    
    # Execute query
    cursor = report_collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    
    # Convert results
    reports = []
    for report in cursor:
        report["id"] = str(report.pop("_id"))
        reports.append(report)
    
    return reports


def count_reports(
    user_id: str,
    report_type: Optional[ReportType] = None,
    time_range: Optional[TimeRange] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> int:
    """
    Count reports with filtering
    """
    # Build query
    query = {"created_by": user_id}
    
    if report_type:
        query["params.report_type"] = report_type
        
    if time_range:
        query["params.time_range"] = time_range
        
    if start_date and end_date:
        query["created_at"] = {
            "$gte": start_date,
            "$lte": end_date
        }
    
    # Execute count
    return report_collection.count_documents(query)


def update_report_status(report_id: str, status: str, result_url: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Update report status
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(report_id)
    except:
        return None
    
    # Prepare update
    update = {
        "status": status,
        "updated_at": datetime.utcnow()
    }
    
    if result_url:
        update["result_url"] = result_url
    
    # Update report
    report_collection.update_one(
        {"_id": object_id},
        {"$set": update}
    )
    
    # Get updated report
    return get_report(report_id)


def delete_report(report_id: str) -> bool:
    """
    Delete a report
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(report_id)
    except:
        return False
    
    # Delete report
    result = report_collection.delete_one({"_id": object_id})
    
    return result.deleted_count > 0