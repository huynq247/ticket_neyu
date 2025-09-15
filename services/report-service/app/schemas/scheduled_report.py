from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

# Schedule schema
class ReportSchedule(BaseModel):
    frequency: str = Field(..., description="Frequency of report generation (one_time, daily, weekly, monthly)")
    start_date: Optional[str] = Field(None, description="Start date for scheduled reports (ISO format)")
    end_date: Optional[str] = Field(None, description="End date for scheduled reports (ISO format)")
    time_of_day: Optional[str] = Field(None, description="Time of day to generate report (HH:MM format)")
    day_of_week: Optional[int] = Field(None, description="Day of week for weekly reports (0-6, where 0 is Monday)")
    day_of_month: Optional[int] = Field(None, description="Day of month for monthly reports (1-31)")

# Base scheduled report schema
class ScheduledReportBase(BaseModel):
    name: str = Field(..., description="Name of the scheduled report")
    description: Optional[str] = Field(None, description="Description of the scheduled report")
    report_type: str = Field(..., description="Type of report to generate")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for report generation")
    schedule: ReportSchedule = Field(..., description="Schedule information")
    export_formats: List[str] = Field(default=["json"], description="Export formats for the report")
    template_id: Optional[str] = Field(None, description="ID of template to use for rendering")
    send_notification: bool = Field(False, description="Whether to send notification when report is generated")
    notification_email: Optional[str] = Field(None, description="Email to send notification to")
    active: bool = Field(True, description="Whether the scheduled report is active")

# Create schema
class ScheduledReportCreate(ScheduledReportBase):
    pass

# Update schema
class ScheduledReportUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the scheduled report")
    description: Optional[str] = Field(None, description="Description of the scheduled report")
    params: Optional[Dict[str, Any]] = Field(None, description="Parameters for report generation")
    schedule: Optional[ReportSchedule] = Field(None, description="Schedule information")
    export_formats: Optional[List[str]] = Field(None, description="Export formats for the report")
    template_id: Optional[str] = Field(None, description="ID of template to use for rendering")
    send_notification: Optional[bool] = Field(None, description="Whether to send notification when report is generated")
    notification_email: Optional[str] = Field(None, description="Email to send notification to")
    active: Optional[bool] = Field(None, description="Whether the scheduled report is active")

# Response schema
class ScheduledReport(ScheduledReportBase):
    id: str = Field(..., description="ID of the scheduled report")
    job_id: Optional[str] = Field(None, description="ID of the scheduled job")
    created_by: str = Field(..., description="ID of the user who created the report")
    created_at: str = Field(..., description="Creation timestamp (ISO format)")
    updated_at: str = Field(..., description="Last update timestamp (ISO format)")

    class Config:
        from_attributes = True

# List response schema
class ScheduledReportList(BaseModel):
    total: int = Field(..., description="Total number of scheduled reports")
    scheduled_reports: List[ScheduledReport] = Field(..., description="List of scheduled reports")