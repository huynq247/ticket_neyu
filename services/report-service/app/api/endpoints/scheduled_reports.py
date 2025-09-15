from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Optional, List, Dict, Any

from app.api.deps import get_current_user
from app.models.scheduled_report import (
    create_scheduled_report,
    get_scheduled_report,
    update_scheduled_report,
    list_scheduled_reports,
    count_scheduled_reports,
    delete_scheduled_report
)
from app.schemas.report import (
    ScheduledReportCreate,
    ScheduledReportUpdate,
    ScheduledReport,
    ScheduledReportList
)

router = APIRouter()


@router.post("/", response_model=ScheduledReport, status_code=status.HTTP_201_CREATED)
async def create_new_scheduled_report(
    report_data: ScheduledReportCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new scheduled report
    """
    report = create_scheduled_report(report_data, current_user["id"])
    if not report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create scheduled report"
        )
    
    return report


@router.get("/{report_id}", response_model=ScheduledReport)
async def get_scheduled_report_by_id(
    report_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a scheduled report by ID
    """
    report = get_scheduled_report(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled report not found"
        )
    
    # Check if user has access to this report
    if report["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this scheduled report"
        )
    
    return report


@router.put("/{report_id}", response_model=ScheduledReport)
async def update_scheduled_report_by_id(
    report_data: ScheduledReportUpdate,
    report_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update a scheduled report
    """
    existing = get_scheduled_report(report_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled report not found"
        )
    
    # Check if user has access to this report
    if existing["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this scheduled report"
        )
    
    updated = update_scheduled_report(report_id, report_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update scheduled report"
        )
    
    return updated


@router.get("/", response_model=ScheduledReportList)
async def get_scheduled_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    active_only: bool = False,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get scheduled reports for current user
    """
    reports = list_scheduled_reports(
        user_id=current_user["id"],
        skip=skip,
        limit=limit,
        active_only=active_only
    )
    
    total = count_scheduled_reports(
        user_id=current_user["id"],
        active_only=active_only
    )
    
    return {
        "total": total,
        "scheduled_reports": reports
    }


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheduled_report_by_id(
    report_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete a scheduled report
    """
    existing = get_scheduled_report(report_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled report not found"
        )
    
    # Check if user has access to this report
    if existing["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this scheduled report"
        )
    
    success = delete_scheduled_report(report_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting scheduled report"
        )
    
    return None