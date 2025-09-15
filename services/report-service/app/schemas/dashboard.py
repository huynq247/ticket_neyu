from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from app.schemas.report import ReportParams, TimeRange


class ChartType(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    DONUT = "donut"
    AREA = "area"
    SCATTER = "scatter"
    TABLE = "table"
    CARD = "card"  # For single value display


class WidgetSize(str, Enum):
    SMALL = "small"  # 1x1
    MEDIUM = "medium"  # 2x1
    LARGE = "large"  # 2x2
    EXTRA_LARGE = "extra_large"  # 4x2


class WidgetConfig(BaseModel):
    title: str
    chart_type: ChartType
    size: WidgetSize = WidgetSize.MEDIUM
    report_params: ReportParams
    position: Dict[str, int] = {"row": 0, "col": 0}
    config: Dict[str, Any] = {}  # Chart specific configuration


class DashboardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    time_range: TimeRange = TimeRange.MONTHLY
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    refresh_interval: Optional[int] = None  # In minutes, None for manual refresh
    widgets: List[WidgetConfig] = []


class DashboardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    time_range: Optional[TimeRange] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    refresh_interval: Optional[int] = None
    widgets: Optional[List[WidgetConfig]] = None


class Dashboard(DashboardCreate):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DashboardList(BaseModel):
    total: int
    dashboards: List[Dashboard]