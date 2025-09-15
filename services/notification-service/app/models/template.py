from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.core.database import template_collection
from app.schemas.template import TemplateCreate, TemplateUpdate


def create_template(template_data: TemplateCreate) -> Dict[str, Any]:
    """
    Create a new template record in the database
    
    Args:
        template_data: Template data
        
    Returns:
        Created template document
    """
    template_dict = template_data.model_dump()
    
    # Add additional fields
    template_dict["created_at"] = datetime.utcnow()
    template_dict["updated_at"] = datetime.utcnow()
    
    # Check if template with same name already exists
    existing = template_collection.find_one({"name": template_data.name})
    if existing:
        return None
    
    # Insert into database
    result = template_collection.insert_one(template_dict)
    
    # Get the inserted document
    return get_template(result.inserted_id)


def get_template(template_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a template by ID
    
    Args:
        template_id: ID of the template
        
    Returns:
        Template document if found, None otherwise
    """
    if isinstance(template_id, str):
        try:
            template_id = ObjectId(template_id)
        except:
            return None
            
    return template_collection.find_one({"_id": template_id})


def get_template_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Get a template by name
    
    Args:
        name: Name of the template
        
    Returns:
        Template document if found, None otherwise
    """
    return template_collection.find_one({"name": name})


def update_template(template_id: str, update_data: TemplateUpdate) -> Optional[Dict[str, Any]]:
    """
    Update a template record
    
    Args:
        template_id: ID of the template to update
        update_data: New data for the template
        
    Returns:
        Updated template document if found and updated, None otherwise
    """
    template = get_template(template_id)
    if not template:
        return None
        
    # Convert to ObjectId
    if isinstance(template_id, str):
        template_id = ObjectId(template_id)
    
    # Prepare update data
    update_dict = update_data.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    # Update in database
    template_collection.update_one(
        {"_id": template_id},
        {"$set": update_dict}
    )
    
    # Return updated document
    return get_template(template_id)


def delete_template(template_id: str) -> bool:
    """
    Delete a template record
    
    Args:
        template_id: ID of the template to delete
        
    Returns:
        True if deleted, False otherwise
    """
    template = get_template(template_id)
    if not template:
        return False
        
    # Convert to ObjectId
    if isinstance(template_id, str):
        template_id = ObjectId(template_id)
        
    # Delete from database
    result = template_collection.delete_one({"_id": template_id})
    
    return result.deleted_count > 0


def list_templates(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    template_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List templates with filtering options
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        name: Filter by template name
        template_type: Filter by template type
        
    Returns:
        List of template documents
    """
    # Build query
    query = {}
    
    if name:
        # Case-insensitive partial matching for name
        query["name"] = {"$regex": name, "$options": "i"}
        
    if template_type:
        query["type"] = template_type
        
    # Execute query
    cursor = template_collection.find(query).skip(skip).limit(limit).sort("name", 1)
    
    return list(cursor)


def count_templates(
    name: Optional[str] = None,
    template_type: Optional[str] = None
) -> int:
    """
    Count templates with filtering options
    
    Args:
        name: Filter by template name
        template_type: Filter by template type
        
    Returns:
        Number of matching templates
    """
    # Build query
    query = {}
    
    if name:
        # Case-insensitive partial matching for name
        query["name"] = {"$regex": name, "$options": "i"}
        
    if template_type:
        query["type"] = template_type
        
    # Execute count
    return template_collection.count_documents(query)