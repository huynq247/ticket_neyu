from fastapi import APIRouter

from app.api.endpoints import users, auth, roles, departments, permissions

api_router = APIRouter()

# Include routers for different endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])