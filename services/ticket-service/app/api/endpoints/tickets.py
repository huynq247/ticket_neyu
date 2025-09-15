from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, Path

from app.db.mongodb import MongoDB, TicketDocument, CategoryDocument, CommentDocument
from app.schemas.ticket import (
    Ticket,
    TicketCreate,
    TicketUpdate,
    TicketListResponse,
    TicketWithCategory,
    TicketStatus
)

router = APIRouter()


@router.get("/", response_model=TicketListResponse)
async def get_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[TicketStatus] = None,
    requester_id: Optional[str] = None,
    assignee_id: Optional[str] = None,
    category_id: Optional[str] = None,
):
    """
    Get tickets with optional filtering
    """
    # Prepare filter
    filter_query = {}
    if status:
        filter_query["status"] = status
    if requester_id:
        filter_query["requester_id"] = requester_id
    if assignee_id:
        filter_query["assignee_id"] = assignee_id
    if category_id:
        filter_query["category_id"] = ObjectId(category_id)
    
    # Get tickets from database
    collection = TicketDocument.get_collection()
    total = collection.count_documents(filter_query)
    cursor = collection.find(filter_query).skip(skip).limit(limit).sort("created_at", -1)
    
    # Convert to response format
    items = [TicketDocument.to_dict(ticket) for ticket in cursor]
    
    return {"total": total, "items": items}


@router.post("/", response_model=Ticket)
async def create_ticket(ticket_in: TicketCreate):
    """
    Create a new ticket
    """
    # Check if category exists
    category_collection = CategoryDocument.get_collection()
    category = category_collection.find_one({"_id": ObjectId(ticket_in.category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Create ticket document
    now = datetime.utcnow()
    ticket_data = ticket_in.dict()
    ticket_data["status"] = TicketStatus.OPEN
    ticket_data["created_at"] = now
    ticket_data["updated_at"] = now
    ticket_data["category_id"] = ObjectId(ticket_in.category_id)
    
    # Insert ticket
    collection = TicketDocument.get_collection()
    result = collection.insert_one(ticket_data)
    
    # Get created ticket
    created_ticket = collection.find_one({"_id": result.inserted_id})
    
    return TicketDocument.to_dict(created_ticket)


@router.get("/{ticket_id}", response_model=TicketWithCategory)
async def get_ticket(ticket_id: str = Path(...)):
    """
    Get ticket by ID with category
    """
    # Get ticket
    collection = TicketDocument.get_collection()
    ticket = collection.find_one({"_id": ObjectId(ticket_id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Get category
    category_collection = CategoryDocument.get_collection()
    category = category_collection.find_one({"_id": ticket["category_id"]})
    
    # Get comments
    comment_collection = CommentDocument.get_collection()
    comments = list(comment_collection.find({"ticket_id": ObjectId(ticket_id)}).sort("created_at", 1))
    comments = [CommentDocument.to_dict(comment) for comment in comments]
    
    # Convert to response format
    ticket = TicketDocument.to_dict(ticket)
    ticket["category"] = CategoryDocument.to_dict(category)
    ticket["comments"] = comments
    
    return ticket


@router.put("/{ticket_id}", response_model=Ticket)
async def update_ticket(ticket_id: str, ticket_in: TicketUpdate):
    """
    Update ticket
    """
    # Check if ticket exists
    collection = TicketDocument.get_collection()
    ticket = collection.find_one({"_id": ObjectId(ticket_id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Prepare update data
    update_data = ticket_in.dict(exclude_unset=True)
    if "category_id" in update_data and update_data["category_id"]:
        # Check if category exists
        category_collection = CategoryDocument.get_collection()
        category = category_collection.find_one({"_id": ObjectId(update_data["category_id"])})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        update_data["category_id"] = ObjectId(update_data["category_id"])
    
    # Update ticket
    update_data["updated_at"] = datetime.utcnow()
    collection.update_one({"_id": ObjectId(ticket_id)}, {"$set": update_data})
    
    # Get updated ticket
    updated_ticket = collection.find_one({"_id": ObjectId(ticket_id)})
    
    return TicketDocument.to_dict(updated_ticket)


@router.delete("/{ticket_id}", response_model=Dict[str, Any])
async def delete_ticket(ticket_id: str):
    """
    Delete ticket and related comments
    """
    # Check if ticket exists
    collection = TicketDocument.get_collection()
    ticket = collection.find_one({"_id": ObjectId(ticket_id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Delete ticket
    collection.delete_one({"_id": ObjectId(ticket_id)})
    
    # Delete related comments
    comment_collection = CommentDocument.get_collection()
    comment_collection.delete_many({"ticket_id": ObjectId(ticket_id)})
    
    return {"message": "Ticket deleted successfully"}