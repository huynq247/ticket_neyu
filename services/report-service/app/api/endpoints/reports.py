from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.api.deps import get_current_user
from app.models.report import (
    create_report, 
    get_report, 
    list_reports, 
    count_reports, 
    update_report_status,
    delete_report
)
from app.analytics.generator import generate_report
from app.schemas.report import (
    ReportCreate, 
    Report, 
    ReportList, 
    ReportType, 
    ReportFormat, 
    TimeRange
)

router = APIRouter()


@router.post("/", response_model=Report, status_code=status.HTTP_201_CREATED)
async def create_new_report(
    report_data: ReportCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new report
    """
    # Create report in database
    report = create_report(report_data, current_user["id"])
    if not report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create report"
        )
    
    # Generate report asynchronously
    # In a real implementation, this would be a background task
    # or a call to a worker queue
    try:
        report = await generate_report(report["id"])
    except Exception as e:
        update_report_status(report["id"], "failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )
    
    return report


@router.get("/{report_id}", response_model=Report)
async def get_report_by_id(
    report_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a report by ID
    """
    report = get_report(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Check if user has access to this report
    if report["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this report"
        )
    
    return report


@router.get("/", response_model=ReportList)
async def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    report_type: Optional[ReportType] = None,
    time_range: Optional[TimeRange] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get reports with filtering
    """
    reports = list_reports(
        user_id=current_user["id"],
        skip=skip,
        limit=limit,
        report_type=report_type,
        time_range=time_range,
        start_date=start_date,
        end_date=end_date
    )
    
    total = count_reports(
        user_id=current_user["id"],
        report_type=report_type,
        time_range=time_range,
        start_date=start_date,
        end_date=end_date
    )
    
    return {
        "total": total,
        "reports": reports
    }


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report_by_id(
    report_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete a report
    """
    report = get_report(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Check if user has access to this report
    if report["created_by"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this report"
        )
    
    success = delete_report(report_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting report"
        )
    
    return None