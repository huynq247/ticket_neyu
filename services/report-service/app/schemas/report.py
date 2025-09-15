from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ReportType(str, Enum):
    TICKET_SUMMARY = "ticket_summary"
    USER_ACTIVITY = "user_activity"
    RESPONSE_TIME = "response_time"
    RESOLUTION_TIME = "resolution_time"
    SATISFACTION = "satisfaction"
    WORKLOAD = "workload"
    CUSTOM = "custom"


class ReportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"
    HTML = "html"


class TimeRange(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class FilterOperator(str, Enum):
    EQ = "eq"  # Equals
    NE = "ne"  # Not equals
    GT = "gt"  # Greater than
    GTE = "gte"  # Greater than or equal
    LT = "lt"  # Less than
    LTE = "lte"  # Less than or equal
    IN = "in"  # In list
    NIN = "nin"  # Not in list
    CONTAINS = "contains"  # Contains string
    STARTS_WITH = "starts_with"  # Starts with
    ENDS_WITH = "ends_with"  # Ends with


class ScheduleFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class FilterCondition(BaseModel):
    field: str
    operator: FilterOperator
    value: Any


class SortField(BaseModel):
    field: str
    direction: str = "asc"  # asc or desc


class ReportFilter(BaseModel):
    conditions: List[FilterCondition] = []
    sort: Optional[List[SortField]] = None
    limit: Optional[int] = None


class ReportParams(BaseModel):
    report_type: ReportType
    time_range: TimeRange
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    filters: Optional[ReportFilter] = None
    aggregation: Optional[str] = None
    group_by: Optional[List[str]] = None


class ReportCreate(BaseModel):
    name: str
    description: Optional[str] = None
    params: ReportParams
    template_id: Optional[str] = None
    format: ReportFormat = ReportFormat.JSON


class ReportTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    report_type: ReportType
    params: Dict[str, Any] = {}
    query_template: str
    formats: List[ReportFormat] = [ReportFormat.JSON]


class ReportTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    query_template: Optional[str] = None
    formats: Optional[List[ReportFormat]] = None


class ScheduledReportCreate(BaseModel):
    name: str
    description: Optional[str] = None
    report_params: ReportParams
    template_id: Optional[str] = None
    frequency: ScheduleFrequency
    day_of_week: Optional[int] = None  # 0-6, where 0 is Monday
    day_of_month: Optional[int] = None  # 1-31
    hour: int
    minute: int
    format: ReportFormat = ReportFormat.PDF
    recipients: List[str]  # Email addresses


class ScheduledReportUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    report_params: Optional[ReportParams] = None
    frequency: Optional[ScheduleFrequency] = None
    day_of_week: Optional[int] = None
    day_of_month: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    format: Optional[ReportFormat] = None
    recipients: Optional[List[str]] = None
    active: Optional[bool] = None


class ReportTemplate(ReportTemplateCreate):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Report(ReportCreate):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    status: str
    result_url: Optional[str] = None

    class Config:
        orm_mode = True


class ScheduledReport(ScheduledReportCreate):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    next_run: datetime
    last_run: Optional[datetime] = None
    active: bool = True

    class Config:
        orm_mode = True


class ReportTemplateList(BaseModel):
    total: int
    templates: List[ReportTemplate]


class ReportList(BaseModel):
    total: int
    reports: List[Report]


class ScheduledReportList(BaseModel):
    total: int
    scheduled_reports: List[ScheduledReport]