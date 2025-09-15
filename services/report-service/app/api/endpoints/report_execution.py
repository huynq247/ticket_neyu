from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from fastapi import status
from typing import Dict, Any, Optional, List

from app.api.deps import get_current_user
from app.analytics.report_generator import generate_report_by_type
from app.analytics.report_exporter import export_report, SUPPORTED_FORMATS
from app.analytics.scheduler import generate_and_save_report
from app.models.report import get_report
from app.models.template import get_template

router = APIRouter()


@router.post("/generate")
async def generate_report(
    report_type: str = Query(..., description="Type of report to generate"),
    days: int = Query(30, description="Number of days to include in the report"),
    export_format: str = Query("json", description=f"Export format. Supported: {', '.join(SUPPORTED_FORMATS)}"),
    save: bool = Query(False, description="Whether to save the report to the database"),
    background_tasks: BackgroundTasks = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    template_id: Optional[str] = Query(None, description="Template ID to use for rendering")
):
    """
    Generate a report on demand
    
    This endpoint generates a report based on the specified type and parameters.
    The report can be returned directly or saved to the database.
    """
    # Check if export format is supported
    if export_format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported export format: {export_format}. Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    # Prepare parameters
    params = {
        "days": days
    }
    
    # If saving to database, use background task
    if save and background_tasks:
        # Schedule the report generation in the background
        background_tasks.add_task(
            generate_and_save_report,
            report_type=report_type,
            params=params,
            user_id=current_user["id"],
            template_id=template_id,
            export_formats=[export_format],
            send_notification=False
        )
        
        return {
            "message": "Report generation scheduled",
            "report_type": report_type,
            "params": params
        }
    
    # Generate report directly
    report_data = await generate_report_by_type(report_type, **params)
    
    if "error" in report_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {report_data['error']}"
        )
    
    # Get template path if template_id is provided
    template_path = None
    if template_id and export_format in ["html", "pdf"]:
        template = get_template(template_id)
        if template and "template_path" in template:
            template_path = template["template_path"]
    
    # Export to requested format
    export_result = export_report(report_data, export_format, template_path)
    
    if "error" in export_result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting report: {export_result['error']}"
        )
    
    # Return the export result
    return export_result


@router.get("/download/{report_id}")
async def download_report(
    report_id: str = Path(..., description="ID of the report to download"),
    export_format: str = Query("json", description=f"Export format. Supported: {', '.join(SUPPORTED_FORMATS)}"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Download a previously generated report in the specified format
    """
    # Check if export format is supported
    if export_format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported export format: {export_format}. Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    # Get the report
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
    
    # Check if export is already available
    if "exports" in report and export_format in report["exports"]:
        return report["exports"][export_format]
    
    # If not, generate the export
    report_data = report.get("data", {})
    
    # Get template path if template_id is provided
    template_path = None
    if "template_id" in report and report["template_id"] and export_format in ["html", "pdf"]:
        template = get_template(report["template_id"])
        if template and "template_path" in template:
            template_path = template["template_path"]
    
    # Export to requested format
    export_result = export_report(report_data, export_format, template_path)
    
    if "error" in export_result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting report: {export_result['error']}"
        )
    
    # Return the export result
    return export_result