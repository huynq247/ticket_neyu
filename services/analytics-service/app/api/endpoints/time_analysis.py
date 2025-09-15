from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
from pydantic import BaseModel

from app.db.database import get_db
from app.analytics.aggregation import DataAggregator
from app.schemas.analytics import (
    TimeGranularity, AggregationDimension, AggregationMetric,
    TimeSeriesResponse, MetricValue
)
from app.visualization.visualizer import DataVisualizer

router = APIRouter()

class TimeRangeParams(BaseModel):
    start_date: datetime
    end_date: datetime
    granularity: TimeGranularity = TimeGranularity.DAY
    
class TimeSeriesRequest(BaseModel):
    time_range: TimeRangeParams
    metrics: List[AggregationMetric]
    filters: Optional[Dict[str, Any]] = None
    include_visualization: bool = False

@router.post("/trend", response_model=TimeSeriesResponse)
async def get_time_series_data(
    request: TimeSeriesRequest,
    db: Session = Depends(get_db)
):
    """
    Retrieve time series data for analysis over time.
    
    - **time_range**: Time range parameters (start_date, end_date, granularity)
    - **metrics**: List of metrics to analyze over time
    - **filters**: Optional filters to apply to the data
    - **include_visualization**: Whether to include visualization data
    
    Returns time series data for the specified metrics and time range.
    """
    try:
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Get time series data for each metric
        series_data = []
        
        for metric in request.metrics:
            # Aggregate data over time
            dimensions = [AggregationDimension.TIME]
            df = aggregator.aggregate_ticket_metrics(
                metrics=[metric],
                dimensions=dimensions,
                start_date=request.time_range.start_date,
                end_date=request.time_range.end_date,
                filters=request.filters,
                time_granularity=request.time_range.granularity,
                sort_by="time"  # Sort by time for time series
            )
            
            # Format the results
            time_column = None
            if request.time_range.granularity == TimeGranularity.DAY:
                time_column = "date"
            elif request.time_range.granularity == TimeGranularity.WEEK:
                time_column = "week"
            elif request.time_range.granularity == TimeGranularity.MONTH:
                time_column = "month"
            elif request.time_range.granularity == TimeGranularity.QUARTER:
                time_column = "quarter"
            elif request.time_range.granularity == TimeGranularity.YEAR:
                time_column = "year"
            
            # Get the metric column name
            metric_column = metric.value.lower()
            
            # Build time series data
            values = []
            for _, row in df.iterrows():
                values.append(
                    MetricValue(
                        timestamp=row[time_column].isoformat() if isinstance(row[time_column], datetime) else str(row[time_column]),
                        value=float(row[metric_column]) if row[metric_column] is not None else 0.0
                    )
                )
            
            series_data.append({
                "metric": metric,
                "values": values
            })
        
        # Generate visualization if requested
        visualization_data = None
        if request.include_visualization:
            visualizer = DataVisualizer()
            
            # Prepare data for visualization
            if series_data:
                # Create a combined dataframe for visualization
                import pandas as pd
                viz_data = []
                
                for series in series_data:
                    for value in series["values"]:
                        viz_data.append({
                            "timestamp": value.timestamp,
                            "value": value.value,
                            "metric": series["metric"].value
                        })
                
                viz_df = pd.DataFrame(viz_data)
                
                # Create the visualization
                visualization_data = visualizer.create_line_chart(
                    df=viz_df,
                    x_column="timestamp",
                    y_columns=list(set([series["metric"].value for series in series_data])),
                    title=f"Time Series Analysis ({request.time_range.granularity.value})",
                    x_label="Time",
                    y_label="Value",
                    interactive=True,
                    output_format="json"
                )
        
        return TimeSeriesResponse(
            time_range={
                "start_date": request.time_range.start_date.isoformat(),
                "end_date": request.time_range.end_date.isoformat(),
                "granularity": request.time_range.granularity
            },
            series=series_data,
            visualization=visualization_data
        )
    
    except Exception as e:
        logging.error(f"Error retrieving time series data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving time series data: {str(e)}")

@router.get("/periods/compare", response_model=Dict[str, Any])
async def compare_time_periods(
    metric: AggregationMetric,
    current_start: datetime = Query(...),
    current_end: datetime = Query(...),
    previous_start: Optional[datetime] = None,
    previous_end: Optional[datetime] = None,
    granularity: TimeGranularity = TimeGranularity.DAY,
    filters: Optional[Dict[str, Any]] = None,
    include_visualization: bool = False,
    db: Session = Depends(get_db)
):
    """
    Compare metrics between two time periods.
    
    - **metric**: Metric to compare
    - **current_start**: Start date of the current period
    - **current_end**: End date of the current period
    - **previous_start**: Optional start date of the previous period (calculated if not provided)
    - **previous_end**: Optional end date of the previous period (calculated if not provided)
    - **granularity**: Time granularity for the analysis
    - **filters**: Optional filters to apply to the data
    - **include_visualization**: Whether to include visualization data
    
    Returns comparison data between the two time periods.
    """
    try:
        # Calculate previous period if not provided
        if previous_start is None or previous_end is None:
            # Calculate the duration of the current period
            duration = current_end - current_start
            
            # Set previous period to the same duration before the current period
            previous_end = current_start - timedelta(days=1)
            previous_start = previous_end - duration
        
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Get data for current period
        current_df = aggregator.aggregate_ticket_metrics(
            metrics=[metric],
            dimensions=[AggregationDimension.TIME],
            start_date=current_start,
            end_date=current_end,
            filters=filters,
            time_granularity=granularity
        )
        
        # Get data for previous period
        previous_df = aggregator.aggregate_ticket_metrics(
            metrics=[metric],
            dimensions=[AggregationDimension.TIME],
            start_date=previous_start,
            end_date=previous_end,
            filters=filters,
            time_granularity=granularity
        )
        
        # Calculate total values
        metric_column = metric.value.lower()
        current_total = current_df[metric_column].sum() if not current_df.empty else 0
        previous_total = previous_df[metric_column].sum() if not previous_df.empty else 0
        
        # Calculate percentage change
        percentage_change = 0
        if previous_total > 0:
            percentage_change = ((current_total - previous_total) / previous_total) * 100
        
        # Prepare response
        response = {
            "metric": metric,
            "current_period": {
                "start_date": current_start.isoformat(),
                "end_date": current_end.isoformat(),
                "total": float(current_total)
            },
            "previous_period": {
                "start_date": previous_start.isoformat(),
                "end_date": previous_end.isoformat(),
                "total": float(previous_total)
            },
            "comparison": {
                "absolute_change": float(current_total - previous_total),
                "percentage_change": float(percentage_change)
            },
            "granularity": granularity
        }
        
        # Generate visualization if requested
        if include_visualization:
            visualizer = DataVisualizer()
            
            # Prepare data for visualization
            import pandas as pd
            import numpy as np
            
            # Create time points for x-axis
            current_period_length = (current_end - current_start).days + 1
            previous_period_length = (previous_end - previous_start).days + 1
            max_length = max(current_period_length, previous_period_length)
            
            viz_data = {
                "day": np.arange(max_length),
                "current_period": np.zeros(max_length),
                "previous_period": np.zeros(max_length)
            }
            
            # Fill current period data
            for _, row in current_df.iterrows():
                time_column = granularity.value.lower()
                if time_column in row:
                    if isinstance(row[time_column], datetime):
                        day_index = (row[time_column] - current_start).days
                    else:
                        continue
                    
                    if 0 <= day_index < max_length:
                        viz_data["current_period"][day_index] = row[metric_column]
            
            # Fill previous period data
            for _, row in previous_df.iterrows():
                time_column = granularity.value.lower()
                if time_column in row:
                    if isinstance(row[time_column], datetime):
                        day_index = (row[time_column] - previous_start).days
                    else:
                        continue
                    
                    if 0 <= day_index < max_length:
                        viz_data["previous_period"][day_index] = row[metric_column]
            
            # Create dataframe for visualization
            viz_df = pd.DataFrame(viz_data)
            
            # Create the visualization
            visualization = visualizer.create_line_chart(
                df=viz_df,
                x_column="day",
                y_columns=["current_period", "previous_period"],
                title=f"Period Comparison - {metric.value}",
                x_label="Day",
                y_label=metric.value,
                interactive=True,
                output_format="json"
            )
            
            response["visualization"] = visualization
        
        return response
    
    except Exception as e:
        logging.error(f"Error comparing time periods: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error comparing time periods: {str(e)}")

@router.get("/seasonal", response_model=Dict[str, Any])
async def seasonal_analysis(
    metric: AggregationMetric,
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    seasonality: str = Query(..., description="Type of seasonality: daily, weekly, monthly, quarterly"),
    db: Session = Depends(get_db)
):
    """
    Perform seasonal analysis on time series data.
    
    - **metric**: Metric to analyze
    - **start_date**: Start date for the analysis
    - **end_date**: End date for the analysis
    - **seasonality**: Type of seasonality pattern to analyze
    
    Returns seasonal patterns in the data.
    """
    try:
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Get time series data
        dimensions = [AggregationDimension.TIME]
        
        # Determine granularity based on seasonality
        granularity = TimeGranularity.DAY
        if seasonality == "weekly":
            granularity = TimeGranularity.WEEK
        elif seasonality == "monthly":
            granularity = TimeGranularity.MONTH
        elif seasonality == "quarterly":
            granularity = TimeGranularity.QUARTER
        
        df = aggregator.aggregate_ticket_metrics(
            metrics=[metric],
            dimensions=dimensions,
            start_date=start_date,
            end_date=end_date,
            time_granularity=granularity
        )
        
        # Analyze seasonality
        import pandas as pd
        
        # Ensure the data has a datetime index
        time_column = granularity.value.lower()
        metric_column = metric.value.lower()
        
        if time_column in df.columns:
            df = df.set_index(time_column)
        
        # Convert to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df.index):
            df.index = pd.to_datetime(df.index)
        
        # Extract seasonal components
        seasonal_data = {}
        
        if seasonality == "daily":
            # Group by hour of day
            seasonal_data = df.groupby(df.index.hour)[metric_column].mean().to_dict()
            
        elif seasonality == "weekly":
            # Group by day of week
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            seasonal_values = df.groupby(df.index.dayofweek)[metric_column].mean()
            seasonal_data = {days[i]: float(seasonal_values.iloc[i]) for i in range(len(days)) if i < len(seasonal_values)}
            
        elif seasonality == "monthly":
            # Group by day of month
            seasonal_data = df.groupby(df.index.day)[metric_column].mean().to_dict()
            
        elif seasonality == "quarterly":
            # Group by month of quarter
            quarters = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
            for month in range(1, 13):
                quarter = (month - 1) // 3 + 1
                quarters[f"Q{quarter}"].append(month)
            
            seasonal_values = df.groupby(df.index.month)[metric_column].mean()
            
            # Aggregate by quarter
            q_data = {}
            for q, months in quarters.items():
                values = [seasonal_values.get(m, 0) for m in months if m in seasonal_values.index]
                if values:
                    q_data[q] = float(sum(values) / len(values))
                else:
                    q_data[q] = 0.0
            
            seasonal_data = q_data
        
        # Create visualization
        visualizer = DataVisualizer()
        
        # Prepare data for visualization
        viz_data = []
        for key, value in seasonal_data.items():
            viz_data.append({"period": str(key), "value": value})
        
        viz_df = pd.DataFrame(viz_data)
        
        # Create the visualization
        visualization = visualizer.create_bar_chart(
            df=viz_df,
            x_column="period",
            y_column="value",
            title=f"Seasonal Analysis - {metric.value} ({seasonality})",
            x_label="Period",
            y_label=metric.value,
            interactive=True,
            output_format="json"
        )
        
        return {
            "metric": metric,
            "seasonality": seasonality,
            "data": seasonal_data,
            "visualization": visualization
        }
    
    except Exception as e:
        logging.error(f"Error performing seasonal analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error performing seasonal analysis: {str(e)}")