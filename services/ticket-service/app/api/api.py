from fastapi import APIRouter

from app.api.endpoints import tickets, categories, comments

api_router = APIRouter()

# Include routers for different endpoints
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])