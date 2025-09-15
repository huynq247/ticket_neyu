from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, date
from enum import Enum


class TimeGranularity(str, Enum):
    """
    Time granularity for analytics
    """
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class AggregationDimension(str, Enum):
    """
    Dimensions for data aggregation
    """
    TIME = "time"
    USER = "user"
    DEPARTMENT = "department"
    CATEGORY = "category"
    PRIORITY = "priority"
    STATUS = "status"
    CHANNEL = "channel"


class AggregationMetric(str, Enum):
    """
    Metrics for aggregation
    """
    TICKET_COUNT = "ticket_count"
    RESOLUTION_TIME = "resolution_time"
    RESPONSE_TIME = "response_time"
    REOPENED_COUNT = "reopened_count"
    SLA_VIOLATIONS = "sla_violations"
    CUSTOMER_SATISFACTION = "customer_satisfaction"
    FIRST_CONTACT_RESOLUTION = "first_contact_resolution"
    AGENT_UTILIZATION = "agent_utilization"


class ChartType(str, Enum):
    """
    Types of visualizations
    """
    AUTO = "auto"
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    STACKED_BAR = "stacked_bar"
    TABLE = "table"


class DateRange(BaseModel):
    """
    Date range for filtering analytics
    """
    start_date: date = Field(..., description="Start date (inclusive)")
    end_date: date = Field(..., description="End date (inclusive)")


class TicketMetrics(BaseModel):
    """
    Schema for ticket metrics
    """
    total_tickets: int = Field(..., description="Total number of tickets")
    open_tickets: int = Field(..., description="Number of open tickets")
    closed_tickets: int = Field(..., description="Number of closed tickets")
    avg_response_time: Optional[float] = Field(None, description="Average response time in minutes")
    avg_resolution_time: Optional[float] = Field(None, description="Average resolution time in minutes")
    reopened_tickets: int = Field(..., description="Number of reopened tickets")


class UserActivityMetrics(BaseModel):
    """
    Schema for user activity metrics
    """
    user_id: str = Field(..., description="User ID")
    username: Optional[str] = Field(None, description="Username")
    tickets_created: int = Field(..., description="Number of tickets created")
    tickets_closed: int = Field(..., description="Number of tickets closed")
    comments_created: int = Field(..., description="Number of comments created")
    active_time_minutes: float = Field(..., description="Active time in minutes")


class CategoryMetrics(BaseModel):
    """
    Schema for category metrics
    """
    category_id: str = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    ticket_count: int = Field(..., description="Number of tickets in this category")
    avg_resolution_time: Optional[float] = Field(None, description="Average resolution time in minutes")
    open_tickets: int = Field(..., description="Number of open tickets")
    closed_tickets: int = Field(..., description="Number of closed tickets")


class TimeSeriesDataPoint(BaseModel):
    """
    Schema for time series data point
    """
    date: str = Field(..., description="Date or time period")
    value: float = Field(..., description="Value for the data point")


class TimeSeriesData(BaseModel):
    """
    Schema for time series data
    """
    metric: str = Field(..., description="Name of the metric")
    granularity: TimeGranularity = Field(..., description="Time granularity")
    data: List[TimeSeriesDataPoint] = Field(..., description="Time series data points")


class KPIData(BaseModel):
    """
    Schema for KPI data
    """
    name: str = Field(..., description="Name of the KPI")
    value: float = Field(..., description="Current value of the KPI")
    target: Optional[float] = Field(None, description="Target value for the KPI")
    previous_value: Optional[float] = Field(None, description="Previous value of the KPI")
    change_percentage: Optional[float] = Field(None, description="Percentage change from previous value")
    trend: Optional[List[float]] = Field(None, description="Historical trend values")


class DashboardData(BaseModel):
    """
    Schema for dashboard data
    """
    ticket_metrics: TicketMetrics = Field(..., description="Ticket metrics")
    time_series: List[TimeSeriesData] = Field(..., description="Time series data")
    kpis: List[KPIData] = Field(..., description="KPI data")
    top_categories: List[CategoryMetrics] = Field(..., description="Top categories by ticket count")
    top_users: List[UserActivityMetrics] = Field(..., description="Top users by activity")


class AnalyticsQueryParams(BaseModel):
    """
    Query parameters for analytics
    """
    start_date: Optional[date] = Field(None, description="Start date for analytics (inclusive)")
    end_date: Optional[date] = Field(None, description="End date for analytics (inclusive)")
    granularity: TimeGranularity = Field(TimeGranularity.DAY, description="Time granularity")
    categories: Optional[List[str]] = Field(None, description="List of category IDs to filter by")
    priorities: Optional[List[str]] = Field(None, description="List of priority IDs to filter by")
    statuses: Optional[List[str]] = Field(None, description="List of status IDs to filter by")
    users: Optional[List[str]] = Field(None, description="List of user IDs to filter by")
    departments: Optional[List[str]] = Field(None, description="List of departments to filter by")
    
    class Config:
        use_enum_values = True


class ForecastParams(BaseModel):
    """
    Parameters for forecasting
    """
    metric: str = Field(..., description="Metric to forecast (e.g., ticket_count, resolution_time)")
    periods: int = Field(..., description="Number of periods to forecast")
    interval_width: float = Field(0.95, description="Confidence interval width (0-1)")
    granularity: TimeGranularity = Field(TimeGranularity.DAY, description="Time granularity")
    
    class Config:
        use_enum_values = True


class ForecastResult(BaseModel):
    """
    Result of forecasting
    """
    metric: str = Field(..., description="Metric that was forecasted")
    granularity: TimeGranularity = Field(..., description="Time granularity")
    dates: List[str] = Field(..., description="Dates for the forecast periods")
    forecast: List[float] = Field(..., description="Forecasted values")
    lower_bound: List[float] = Field(..., description="Lower bound of confidence interval")
    upper_bound: List[float] = Field(..., description="Upper bound of confidence interval")
    
    class Config:
        use_enum_values = True


class AnomalyDetectionParams(BaseModel):
    """
    Parameters for anomaly detection
    """
    metric: str = Field(..., description="Metric to detect anomalies on")
    sensitivity: float = Field(0.05, description="Sensitivity for anomaly detection (0-1)")
    granularity: TimeGranularity = Field(TimeGranularity.DAY, description="Time granularity")
    
    class Config:
        use_enum_values = True


class AnomalyPoint(BaseModel):
    """
    Anomaly data point
    """
    date: str = Field(..., description="Date of the anomaly")
    value: float = Field(..., description="Value at the anomaly point")
    expected_value: float = Field(..., description="Expected value at this point")
    deviation: float = Field(..., description="Deviation from expected value (percentage)")
    severity: str = Field(..., description="Severity of the anomaly (low, medium, high)")


class AnomalyDetectionResult(BaseModel):
    """
    Result of anomaly detection
    """
    metric: str = Field(..., description="Metric that was analyzed")
    granularity: TimeGranularity = Field(..., description="Time granularity")
    anomalies: List[AnomalyPoint] = Field(..., description="Detected anomalies")
    
    class Config:
        use_enum_values = True


# New schemas for time-based analytics

class MetricValue(BaseModel):
    """
    Schema for a metric value with timestamp
    """
    timestamp: str = Field(..., description="Timestamp for the data point")
    value: float = Field(..., description="Value of the metric")


class TimeSeriesResponse(BaseModel):
    """
    Response schema for time series data
    """
    time_range: Dict[str, Any] = Field(..., description="Time range parameters")
    series: List[Dict[str, Any]] = Field(..., description="Series data for each metric")
    visualization: Optional[Dict[str, Any]] = Field(None, description="Visualization data")


# New schemas for user analytics

class UserMetrics(BaseModel):
    """
    Schema for user performance metrics
    """
    user_id: str = Field(..., description="User ID")
    user_name: Optional[str] = Field(None, description="User name")
    department: Optional[str] = Field(None, description="Department")
    metrics: Dict[str, float] = Field(..., description="Metrics data")


class UserAnalyticsResponse(BaseModel):
    """
    Response schema for user analytics
    """
    users: List[Dict[str, Any]] = Field(..., description="User performance data")
    visualization: Optional[Dict[str, Any]] = Field(None, description="Visualization data")