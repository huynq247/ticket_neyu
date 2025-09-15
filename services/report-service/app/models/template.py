from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.core.database import report_template_collection
from app.schemas.report import ReportTemplateCreate, ReportTemplateUpdate, ReportType


def create_template(template_data: ReportTemplateCreate, user_id: str) -> Dict[str, Any]:
    """
    Create a new report template
    """
    # Check if a template with the same name already exists
    existing = report_template_collection.find_one({"name": template_data.name})
    if existing:
        return None
    
    # Convert to dict
    template_dict = template_data.model_dump()
    
    # Add metadata
    now = datetime.utcnow()
    template_dict["created_by"] = user_id
    template_dict["created_at"] = now
    template_dict["updated_at"] = now
    
    # Insert into database
    result = report_template_collection.insert_one(template_dict)
    
    # Get created document
    created_template = report_template_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string
    if created_template:
        created_template["id"] = str(created_template.pop("_id"))
    
    return created_template


def get_template(template_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a template by ID
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(template_id)
    except:
        return None
    
    # Find template
    template = report_template_collection.find_one({"_id": object_id})
    
    # Convert ObjectId to string
    if template:
        template["id"] = str(template.pop("_id"))
    
    return template


def get_template_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Get a template by name
    """
    # Find template
    template = report_template_collection.find_one({"name": name})
    
    # Convert ObjectId to string
    if template:
        template["id"] = str(template.pop("_id"))
    
    return template


def update_template(template_id: str, template_data: ReportTemplateUpdate) -> Optional[Dict[str, Any]]:
    """
    Update a template
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(template_id)
    except:
        return None
    
    # Get template to update
    template = report_template_collection.find_one({"_id": object_id})
    if not template:
        return None
    
    # Check name uniqueness if name is being updated
    if template_data.name and template_data.name != template["name"]:
        existing = report_template_collection.find_one({"name": template_data.name})
        if existing:
            return None
    
    # Convert to dict and remove None values
    update_data = {k: v for k, v in template_data.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        return get_template(template_id)
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update template
    report_template_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )
    
    # Get updated template
    return get_template(template_id)


def list_templates(
    skip: int = 0,
    limit: int = 20,
    report_type: Optional[ReportType] = None,
    user_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List templates with filtering
    """
    # Build query
    query = {}
    
    if report_type:
        query["report_type"] = report_type
        
    if user_id:
        query["created_by"] = user_id
    
    # Execute query
    cursor = report_template_collection.find(query).skip(skip).limit(limit).sort("name", 1)
    
    # Convert results
    templates = []
    for template in cursor:
        template["id"] = str(template.pop("_id"))
        templates.append(template)
    
    return templates


def count_templates(
    report_type: Optional[ReportType] = None,
    user_id: Optional[str] = None
) -> int:
    """
    Count templates with filtering
    """
    # Build query
    query = {}
    
    if report_type:
        query["report_type"] = report_type
        
    if user_id:
        query["created_by"] = user_id
    
    # Execute count
    return report_template_collection.count_documents(query)


def delete_template(template_id: str) -> bool:
    """
    Delete a template
    """
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(template_id)
    except:
        return False
    
    # Delete template
    result = report_template_collection.delete_one({"_id": object_id})
    
    return result.deleted_count > 0