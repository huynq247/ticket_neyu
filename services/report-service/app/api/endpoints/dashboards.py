from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Optional, List, Dict, Any

from app.api.deps import get_current_user
from app.models.dashboard import (
    create_dashboard,
    get_dashboard,
    update_dashboard,
    list_dashboards,
    count_dashboards,
    delete_dashboard
)
from app.schemas.dashboard import (
    DashboardCreate,
    DashboardUpdate,
    Dashboard,
    DashboardList
)

router = APIRouter()


@router.post("/", response_model=Dashboard, status_code=status.HTTP_201_CREATED)
async def create_new_dashboard(
    dashboard_data: DashboardCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new dashboard
    """
    dashboard = create_dashboard(dashboard_data, current_user["id"])
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create dashboard"
        )
    
    return dashboard


@router.get("/{dashboard_id}", response_model=Dashboard)
async def get_dashboard_by_id(
    dashboard_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a dashboard by ID
    """
    dashboard = get_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    # Check if user has access to this dashboard
    if dashboard["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this dashboard"
        )
    
    return dashboard


@router.put("/{dashboard_id}", response_model=Dashboard)
async def update_dashboard_by_id(
    dashboard_data: DashboardUpdate,
    dashboard_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update a dashboard
    """
    existing = get_dashboard(dashboard_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    # Check if user has access to this dashboard
    if existing["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this dashboard"
        )
    
    updated = update_dashboard(dashboard_id, dashboard_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update dashboard"
        )
    
    return updated


@router.get("/", response_model=DashboardList)
async def get_dashboards(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get dashboards for current user
    """
    dashboards = list_dashboards(
        user_id=current_user["id"],
        skip=skip,
        limit=limit
    )
    
    total = count_dashboards(user_id=current_user["id"])
    
    return {
        "total": total,
        "dashboards": dashboards
    }


@router.delete("/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dashboard_by_id(
    dashboard_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete a dashboard
    """
    existing = get_dashboard(dashboard_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    # Check if user has access to this dashboard
    if existing["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this dashboard"
        )
    
    success = delete_dashboard(dashboard_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting dashboard"
        )
    
    return None