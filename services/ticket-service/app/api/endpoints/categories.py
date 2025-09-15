from datetime import datetime
from typing import List, Dict, Any
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path

from app.db.mongodb import MongoDB, CategoryDocument
from app.schemas.ticket import Category, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.get("/", response_model=List[Category])
async def get_categories():
    """
    Get all categories
    """
    collection = CategoryDocument.get_collection()
    categories = collection.find().sort("name", 1)
    
    return [CategoryDocument.to_dict(category) for category in categories]


@router.post("/", response_model=Category)
async def create_category(category_in: CategoryCreate):
    """
    Create a new category
    """
    # Check if category with same name exists
    collection = CategoryDocument.get_collection()
    existing = collection.find_one({"name": category_in.name})
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    # Create category
    now = datetime.utcnow()
    category_data = category_in.dict()
    category_data["created_at"] = now
    category_data["updated_at"] = now
    
    # Insert category
    result = collection.insert_one(category_data)
    
    # Get created category
    created_category = collection.find_one({"_id": result.inserted_id})
    
    return CategoryDocument.to_dict(created_category)


@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: str = Path(...)):
    """
    Get category by ID
    """
    collection = CategoryDocument.get_collection()
    category = collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return CategoryDocument.to_dict(category)


@router.put("/{category_id}", response_model=Category)
async def update_category(category_id: str, category_in: CategoryUpdate):
    """
    Update category
    """
    # Check if category exists
    collection = CategoryDocument.get_collection()
    category = collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if name is being updated and already exists
    if "name" in category_in.dict(exclude_unset=True) and category_in.name != category["name"]:
        existing = collection.find_one({"name": category_in.name})
        if existing:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    # Update category
    update_data = category_in.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    collection.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    
    # Get updated category
    updated_category = collection.find_one({"_id": ObjectId(category_id)})
    
    return CategoryDocument.to_dict(updated_category)


@router.delete("/{category_id}", response_model=Dict[str, Any])
async def delete_category(category_id: str):
    """
    Delete category
    """
    # Check if category exists
    collection = CategoryDocument.get_collection()
    category = collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category is being used in any ticket
    ticket_collection = MongoDB.connect()["tickets"]
    ticket_count = ticket_collection.count_documents({"category_id": ObjectId(category_id)})
    if ticket_count > 0:
        raise HTTPException(status_code=400, detail=f"Cannot delete category that is used in {ticket_count} tickets")
    
    # Delete category
    collection.delete_one({"_id": ObjectId(category_id)})
    
    return {"message": "Category deleted successfully"}