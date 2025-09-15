from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.core.database import file_collection
from app.schemas.file import FileCreate, FileUpdate


def create_file(file_data: FileCreate, file_path: str) -> Dict[str, Any]:
    """
    Create a new file record in the database
    
    Args:
        file_data: File metadata
        file_path: Path where the file is stored
        
    Returns:
        Created file document
    """
    file_dict = file_data.model_dump()
    
    # Add additional fields
    file_dict["path"] = file_path
    file_dict["created_at"] = datetime.utcnow()
    file_dict["updated_at"] = datetime.utcnow()
    
    # Insert into database
    result = file_collection.insert_one(file_dict)
    
    # Get the inserted document
    return get_file(result.inserted_id)


def get_file(file_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a file by ID
    
    Args:
        file_id: ID of the file
        
    Returns:
        File document if found, None otherwise
    """
    if isinstance(file_id, str):
        try:
            file_id = ObjectId(file_id)
        except:
            return None
            
    return file_collection.find_one({"_id": file_id})


def update_file(file_id: str, update_data: FileUpdate) -> Optional[Dict[str, Any]]:
    """
    Update a file record
    
    Args:
        file_id: ID of the file to update
        update_data: New data for the file
        
    Returns:
        Updated file document if found and updated, None otherwise
    """
    file = get_file(file_id)
    if not file:
        return None
        
    # Convert to ObjectId
    if isinstance(file_id, str):
        file_id = ObjectId(file_id)
    
    # Prepare update data
    update_dict = update_data.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    # Update in database
    file_collection.update_one(
        {"_id": file_id},
        {"$set": update_dict}
    )
    
    # Return updated document
    return get_file(file_id)


def delete_file(file_id: str) -> bool:
    """
    Delete a file record
    
    Args:
        file_id: ID of the file to delete
        
    Returns:
        True if deleted, False otherwise
    """
    file = get_file(file_id)
    if not file:
        return False
        
    # Convert to ObjectId
    if isinstance(file_id, str):
        file_id = ObjectId(file_id)
        
    # Delete from database
    result = file_collection.delete_one({"_id": file_id})
    
    return result.deleted_count > 0


def list_files(
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[str] = None,
    ticket_id: Optional[str] = None,
    filename_contains: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List files with filtering options
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        owner_id: Filter by owner ID
        ticket_id: Filter by ticket ID
        filename_contains: Filter by filename containing this string
        
    Returns:
        List of file documents
    """
    # Build query
    query = {}
    
    if owner_id:
        query["owner_id"] = owner_id
        
    if ticket_id:
        query["ticket_id"] = ticket_id
        
    if filename_contains:
        query["filename"] = {"$regex": filename_contains, "$options": "i"}
        
    # Execute query
    cursor = file_collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    
    return list(cursor)


def count_files(
    owner_id: Optional[str] = None,
    ticket_id: Optional[str] = None,
    filename_contains: Optional[str] = None
) -> int:
    """
    Count files with filtering options
    
    Args:
        owner_id: Filter by owner ID
        ticket_id: Filter by ticket ID
        filename_contains: Filter by filename containing this string
        
    Returns:
        Number of matching files
    """
    # Build query
    query = {}
    
    if owner_id:
        query["owner_id"] = owner_id
        
    if ticket_id:
        query["ticket_id"] = ticket_id
        
    if filename_contains:
        query["filename"] = {"$regex": filename_contains, "$options": "i"}
        
    # Execute count
    return file_collection.count_documents(query)