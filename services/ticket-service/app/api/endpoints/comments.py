from datetime import datetime
from typing import List, Dict, Any
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path

from app.db.mongodb import CommentDocument, TicketDocument
from app.schemas.ticket import Comment, CommentCreate

router = APIRouter()


@router.get("/{ticket_id}", response_model=List[Comment])
async def get_comments(ticket_id: str = Path(...)):
    """
    Get comments for a ticket
    """
    # Check if ticket exists
    ticket_collection = TicketDocument.get_collection()
    ticket = ticket_collection.find_one({"_id": ObjectId(ticket_id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Get comments
    collection = CommentDocument.get_collection()
    comments = collection.find({"ticket_id": ObjectId(ticket_id)}).sort("created_at", 1)
    
    return [CommentDocument.to_dict(comment) for comment in comments]


@router.post("/{ticket_id}", response_model=Comment)
async def create_comment(ticket_id: str, comment_in: CommentCreate):
    """
    Create a new comment for a ticket
    """
    # Check if ticket exists
    ticket_collection = TicketDocument.get_collection()
    ticket = ticket_collection.find_one({"_id": ObjectId(ticket_id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Create comment
    now = datetime.utcnow()
    comment_data = comment_in.dict()
    comment_data["ticket_id"] = ObjectId(ticket_id)
    comment_data["created_at"] = now
    comment_data["updated_at"] = now
    
    # Insert comment
    collection = CommentDocument.get_collection()
    result = collection.insert_one(comment_data)
    
    # Get created comment
    created_comment = collection.find_one({"_id": result.inserted_id})
    
    # Update ticket updated_at
    ticket_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"updated_at": now}}
    )
    
    return CommentDocument.to_dict(created_comment)


@router.delete("/{comment_id}", response_model=Dict[str, Any])
async def delete_comment(comment_id: str):
    """
    Delete a comment
    """
    # Check if comment exists
    collection = CommentDocument.get_collection()
    comment = collection.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Delete comment
    collection.delete_one({"_id": ObjectId(comment_id)})
    
    # Update ticket updated_at
    ticket_collection = TicketDocument.get_collection()
    ticket_collection.update_one(
        {"_id": comment["ticket_id"]},
        {"$set": {"updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Comment deleted successfully"}