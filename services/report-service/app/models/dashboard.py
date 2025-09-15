from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.core.database import dashboard_collection
from app.schemas.dashboard import DashboardCreate, DashboardUpdate


def create_dashboard(dashboard_data: DashboardCreate, user_id: str) -> Dict[str, Any]:
    """
    Create a new dashboard
    """
    # Convert to dict
    dashboard_dict = dashboard_data.model_dump()
    
    # Add metadata
    now = datetime.utcnow()
    dashboard_dict["created_by"] = user_id
    dashboard_dict["created_at"] = now
    dashboard_dict["updated_at"] = now
    
    # Insert into database
    result = dashboard_collection.insert_one(dashboard_dict)
    
    # Get created document
    created_dashboard = dashboard_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string
    if created_dashboard:
        created_dashboard["id"] = str(created_dashboard.pop("_id"))
    
    return created_dashboard


def get_dashboard(dashboard_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a dashboard by ID
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(dashboard_id)
    except:
        return None
    
    # Find dashboard
    dashboard = dashboard_collection.find_one({"_id": object_id})
    
    # Convert ObjectId to string
    if dashboard:
        dashboard["id"] = str(dashboard.pop("_id"))
    
    return dashboard


def update_dashboard(dashboard_id: str, dashboard_data: DashboardUpdate) -> Optional[Dict[str, Any]]:
    """
    Update a dashboard
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(dashboard_id)
    except:
        return None
    
    # Get dashboard to update
    dashboard = dashboard_collection.find_one({"_id": object_id})
    if not dashboard:
        return None
    
    # Convert to dict and remove None values
    update_data = {k: v for k, v in dashboard_data.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        return get_dashboard(dashboard_id)
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update dashboard
    dashboard_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )
    
    # Get updated dashboard
    return get_dashboard(dashboard_id)


def list_dashboards(
    user_id: str,
    skip: int = 0,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """
    List dashboards for a user
    """
    # Build query
    query = {"created_by": user_id}
    
    # Execute query
    cursor = dashboard_collection.find(query).skip(skip).limit(limit).sort("name", 1)
    
    # Convert results
    dashboards = []
    for dashboard in cursor:
        dashboard["id"] = str(dashboard.pop("_id"))
        dashboards.append(dashboard)
    
    return dashboards


def count_dashboards(user_id: str) -> int:
    """
    Count dashboards for a user
    """
    # Build query
    query = {"created_by": user_id}
    
    # Execute count
    return dashboard_collection.count_documents(query)


def delete_dashboard(dashboard_id: str) -> bool:
    """
    Delete a dashboard
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(dashboard_id)
    except:
        return False
    
    # Delete dashboard
    result = dashboard_collection.delete_one({"_id": object_id})
    
    return result.deleted_count > 0