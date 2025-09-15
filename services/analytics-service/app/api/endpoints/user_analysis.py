from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from pydantic import BaseModel

from app.db.database import get_db
from app.analytics.aggregation import DataAggregator
from app.schemas.analytics import (
    AggregationDimension, AggregationMetric, UserAnalyticsResponse
)
from app.visualization.visualizer import DataVisualizer

router = APIRouter()

class UserAnalyticsRequest(BaseModel):
    metrics: List[AggregationMetric]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    departments: Optional[List[str]] = None
    limit: int = 10
    include_visualization: bool = False
    
@router.post("/performance", response_model=UserAnalyticsResponse)
async def get_user_performance(
    request: UserAnalyticsRequest,
    db: Session = Depends(get_db)
):
    """
    Retrieve user performance analytics.
    
    - **metrics**: List of metrics to analyze by user
    - **start_date**: Optional start date for the analysis
    - **end_date**: Optional end date for the analysis
    - **departments**: Optional list of departments to filter by
    - **limit**: Maximum number of users to include in the results
    - **include_visualization**: Whether to include visualization data
    
    Returns user performance data for the specified metrics.
    """
    try:
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Apply department filter if provided
        filters = {}
        if request.departments:
            filters["department"] = request.departments
        
        # Get user performance data
        df = aggregator.aggregate_ticket_metrics(
            metrics=request.metrics,
            dimensions=[AggregationDimension.USER],
            start_date=request.start_date,
            end_date=request.end_date,
            filters=filters,
            limit=request.limit
        )
        
        # Format the results
        users_data = []
        
        if not df.empty:
            # Assuming 'user_id' and 'user_name' are columns in the result
            for _, row in df.iterrows():
                user_metrics = {}
                
                # Add all metrics to the user data
                for metric in request.metrics:
                    metric_column = metric.value.lower()
                    if metric_column in df.columns:
                        user_metrics[metric.value] = float(row[metric_column]) if row[metric_column] is not None else 0.0
                
                # Build user data
                user_data = {
                    "user_id": str(row["user_id"]) if "user_id" in row else None,
                    "user_name": row["user_name"] if "user_name" in row else None,
                    "department": row["department"] if "department" in row else None,
                    "metrics": user_metrics
                }
                
                users_data.append(user_data)
        
        # Generate visualization if requested
        visualization_data = None
        if request.include_visualization and users_data:
            visualizer = DataVisualizer()
            
            # Prepare data for visualization
            import pandas as pd
            
            viz_data = []
            for user in users_data:
                user_row = {
                    "user_name": user["user_name"] or f"User {user['user_id']}",
                    "department": user["department"] or "N/A"
                }
                
                # Add metrics to the user row
                for metric_name, metric_value in user["metrics"].items():
                    user_row[metric_name] = metric_value
                
                viz_data.append(user_row)
            
            viz_df = pd.DataFrame(viz_data)
            
            # Create the visualization
            metric_names = [metric.value for metric in request.metrics]
            visualization_data = visualizer.create_horizontal_bar_chart(
                df=viz_df,
                x_columns=metric_names,
                y_column="user_name",
                title=f"User Performance Analysis",
                x_label="Value",
                y_label="User",
                interactive=True,
                output_format="json"
            )
        
        return UserAnalyticsResponse(
            users=users_data,
            visualization=visualization_data
        )
    
    except Exception as e:
        logging.error(f"Error retrieving user performance data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user performance data: {str(e)}")

@router.get("/departments", response_model=Dict[str, Any])
async def get_department_analytics(
    metrics: List[AggregationMetric] = Query(...),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    include_visualization: bool = False,
    db: Session = Depends(get_db)
):
    """
    Retrieve department-level analytics.
    
    - **metrics**: List of metrics to analyze by department
    - **start_date**: Optional start date for the analysis
    - **end_date**: Optional end date for the analysis
    - **include_visualization**: Whether to include visualization data
    
    Returns analytics data aggregated by department.
    """
    try:
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Get department performance data
        df = aggregator.aggregate_ticket_metrics(
            metrics=metrics,
            dimensions=[AggregationDimension.DEPARTMENT],
            start_date=start_date,
            end_date=end_date
        )
        
        # Format the results
        departments_data = []
        
        if not df.empty:
            # Assuming 'department' is a column in the result
            for _, row in df.iterrows():
                dept_metrics = {}
                
                # Add all metrics to the department data
                for metric in metrics:
                    metric_column = metric.value.lower()
                    if metric_column in df.columns:
                        dept_metrics[metric.value] = float(row[metric_column]) if row[metric_column] is not None else 0.0
                
                # Build department data
                dept_data = {
                    "department": row["department"] if "department" in row else "Unknown",
                    "metrics": dept_metrics
                }
                
                departments_data.append(dept_data)
        
        # Generate visualization if requested
        visualization_data = None
        if include_visualization and departments_data:
            visualizer = DataVisualizer()
            
            # Prepare data for visualization
            import pandas as pd
            
            viz_data = []
            for dept in departments_data:
                dept_row = {
                    "department": dept["department"]
                }
                
                # Add metrics to the department row
                for metric_name, metric_value in dept["metrics"].items():
                    dept_row[metric_name] = metric_value
                
                viz_data.append(dept_row)
            
            viz_df = pd.DataFrame(viz_data)
            
            # Create the visualization
            metric_names = [metric.value for metric in metrics]
            visualization_data = visualizer.create_bar_chart(
                df=viz_df,
                x_column="department",
                y_columns=metric_names,
                title=f"Department Performance Analysis",
                x_label="Department",
                y_label="Value",
                interactive=True,
                output_format="json"
            )
        
        return {
            "departments": departments_data,
            "visualization": visualization_data
        }
    
    except Exception as e:
        logging.error(f"Error retrieving department analytics data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving department analytics data: {str(e)}")

@router.get("/top-performers", response_model=Dict[str, Any])
async def get_top_performers(
    metric: AggregationMetric = Query(...),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    department: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve top-performing users for a specific metric.
    
    - **metric**: Metric to rank users by
    - **start_date**: Optional start date for the analysis
    - **end_date**: Optional end date for the analysis
    - **department**: Optional department to filter by
    - **limit**: Maximum number of users to include in the results
    
    Returns a list of top-performing users.
    """
    try:
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Apply department filter if provided
        filters = {}
        if department:
            filters["department"] = [department]
        
        # Get top performers directly from the aggregator
        top_performers = aggregator.get_top_performers(
            metric=metric,
            start_date=start_date,
            end_date=end_date,
            filters=filters,
            limit=limit
        )
        
        # Convert to list of dictionaries
        results = []
        metric_column = metric.value.lower()
        
        for _, row in top_performers.iterrows():
            performer = {
                "user_id": str(row["user_id"]) if "user_id" in row else None,
                "user_name": row["user_name"] if "user_name" in row else None,
                "department": row["department"] if "department" in row else None,
                "value": float(row[metric_column]) if metric_column in row else 0.0
            }
            results.append(performer)
        
        # Create visualization
        visualizer = DataVisualizer()
        
        # Prepare data for visualization
        import pandas as pd
        
        viz_df = pd.DataFrame(results)
        if not viz_df.empty:
            viz_df["user_label"] = viz_df.apply(
                lambda x: x["user_name"] or f"User {x['user_id']}", axis=1
            )
            
            # Create the visualization
            visualization = visualizer.create_horizontal_bar_chart(
                df=viz_df,
                x_column="value",
                y_column="user_label",
                title=f"Top Performers - {metric.value}",
                x_label=metric.value,
                y_label="User",
                interactive=True,
                output_format="json"
            )
        else:
            visualization = None
        
        return {
            "metric": metric,
            "performers": results,
            "visualization": visualization
        }
    
    except Exception as e:
        logging.error(f"Error retrieving top performers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving top performers: {str(e)}")

@router.get("/user-details/{user_id}", response_model=Dict[str, Any])
async def get_user_details(
    user_id: str,
    metrics: List[AggregationMetric] = Query(...),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve detailed analytics for a specific user.
    
    - **user_id**: ID of the user to analyze
    - **metrics**: List of metrics to analyze
    - **start_date**: Optional start date for the analysis
    - **end_date**: Optional end date for the analysis
    
    Returns detailed analytics data for the specified user.
    """
    try:
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Filter for specific user
        filters = {"user_id": [user_id]}
        
        # Get user metrics data
        df = aggregator.aggregate_ticket_metrics(
            metrics=metrics,
            dimensions=[AggregationDimension.USER],
            start_date=start_date,
            end_date=end_date,
            filters=filters
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for user ID: {user_id}")
        
        # Get user information
        user_info = {
            "user_id": user_id,
            "user_name": df["user_name"].iloc[0] if "user_name" in df.columns else None,
            "department": df["department"].iloc[0] if "department" in df.columns else None,
        }
        
        # Get metrics for the user
        user_metrics = {}
        for metric in metrics:
            metric_column = metric.value.lower()
            if metric_column in df.columns:
                user_metrics[metric.value] = float(df[metric_column].iloc[0]) if df[metric_column].iloc[0] is not None else 0.0
        
        # Get user's performance over time
        time_series_data = {}
        
        for metric in metrics:
            # Get time series data for the metric
            time_df = aggregator.aggregate_ticket_metrics(
                metrics=[metric],
                dimensions=[AggregationDimension.TIME, AggregationDimension.USER],
                start_date=start_date,
                end_date=end_date,
                filters=filters,
                time_granularity="DAY"
            )
            
            # Format the results
            values = []
            if not time_df.empty:
                metric_column = metric.value.lower()
                for _, row in time_df.iterrows():
                    values.append({
                        "timestamp": row["date"].isoformat() if "date" in row else None,
                        "value": float(row[metric_column]) if metric_column in row else 0.0
                    })
            
            time_series_data[metric.value] = values
        
        # Create visualizations
        visualizer = DataVisualizer()
        
        # Time series visualization
        time_series_viz = None
        if any(len(values) > 0 for values in time_series_data.values()):
            # Prepare data for visualization
            import pandas as pd
            
            viz_data = []
            for metric_name, values in time_series_data.items():
                for value in values:
                    if value["timestamp"]:
                        viz_data.append({
                            "timestamp": value["timestamp"],
                            "value": value["value"],
                            "metric": metric_name
                        })
            
            if viz_data:
                viz_df = pd.DataFrame(viz_data)
                
                # Create the visualization
                time_series_viz = visualizer.create_line_chart(
                    df=viz_df,
                    x_column="timestamp",
                    y_column="value",
                    group_by="metric",
                    title=f"User Performance Over Time - {user_info['user_name'] or user_id}",
                    x_label="Time",
                    y_label="Value",
                    interactive=True,
                    output_format="json"
                )
        
        # Metrics comparison visualization
        metrics_viz = None
        if user_metrics:
            # Prepare data for visualization
            import pandas as pd
            
            viz_data = []
            for metric_name, value in user_metrics.items():
                viz_data.append({
                    "metric": metric_name,
                    "value": value
                })
            
            viz_df = pd.DataFrame(viz_data)
            
            # Create the visualization
            metrics_viz = visualizer.create_bar_chart(
                df=viz_df,
                x_column="metric",
                y_column="value",
                title=f"User Metrics - {user_info['user_name'] or user_id}",
                x_label="Metric",
                y_label="Value",
                interactive=True,
                output_format="json"
            )
        
        return {
            "user_info": user_info,
            "metrics": user_metrics,
            "time_series": time_series_data,
            "visualizations": {
                "time_series": time_series_viz,
                "metrics": metrics_viz
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving user details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user details: {str(e)}")