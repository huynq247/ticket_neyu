from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import logging
from pydantic import BaseModel, Field

from app.db.database import get_db
from app.analytics.aggregation import DataAggregator
from app.analytics.normalization import DataNormalizer
from app.schemas.analytics import (
    AggregationDimension, AggregationMetric, TimeGranularity,
    ChartType
)
from app.visualization.visualizer import DataVisualizer

router = APIRouter()

class FilterCondition(BaseModel):
    field: str
    operator: str = "eq"  # eq, ne, gt, lt, gte, lte, in, not_in, contains
    value: Union[str, int, float, bool, List[Any]]

class DimensionConfig(BaseModel):
    dimension: AggregationDimension
    time_granularity: Optional[TimeGranularity] = None
    
class CustomAnalyticsRequest(BaseModel):
    metrics: List[AggregationMetric]
    dimensions: List[DimensionConfig]
    filters: Optional[List[FilterCondition]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "desc"
    limit: Optional[int] = None
    include_visualization: bool = True
    visualization_type: Optional[ChartType] = None
    normalization: Optional[Dict[str, Any]] = None
    
class CustomAnalyticsResponse(BaseModel):
    data: List[Dict[str, Any]]
    visualization: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any]

@router.post("", response_model=CustomAnalyticsResponse)
async def custom_analytics(
    request: CustomAnalyticsRequest,
    db: Session = Depends(get_db)
):
    """
    Perform custom analytics with flexible configurations.
    
    - **metrics**: List of metrics to analyze
    - **dimensions**: List of dimensions to group by with optional time granularity
    - **filters**: Optional filter conditions to apply to the data
    - **start_date**: Optional start date for the analysis
    - **end_date**: Optional end date for the analysis
    - **sort_by**: Optional field to sort results by
    - **sort_order**: Optional sort order (asc or desc)
    - **limit**: Optional maximum number of results to return
    - **include_visualization**: Whether to include visualization data
    - **visualization_type**: Optional type of visualization to generate
    - **normalization**: Optional normalization parameters for data preprocessing
    
    Returns custom analytics results based on the specified configuration.
    """
    try:
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Process dimensions
        dimensions = [config.dimension for config in request.dimensions]
        
        # Determine time granularity
        time_granularity = None
        for config in request.dimensions:
            if config.dimension == AggregationDimension.TIME and config.time_granularity:
                time_granularity = config.time_granularity
                break
        
        # Process filters
        filters = {}
        if request.filters:
            for filter_condition in request.filters:
                filters[filter_condition.field] = {
                    "operator": filter_condition.operator,
                    "value": filter_condition.value
                }
        
        # Get analytics data
        df = aggregator.aggregate_ticket_metrics(
            metrics=request.metrics,
            dimensions=dimensions,
            start_date=request.start_date,
            end_date=request.end_date,
            filters=filters,
            time_granularity=time_granularity,
            sort_by=request.sort_by,
            sort_order=request.sort_order,
            limit=request.limit
        )
        
        # Apply normalization if specified
        if request.normalization and df is not None and not df.empty:
            normalizer = DataNormalizer()
            
            for column, config in request.normalization.items():
                if column in df.columns:
                    method = config.get("method", "min_max")
                    params = config.get("params", {})
                    
                    if method == "min_max":
                        df[column] = normalizer.min_max_scale(df[column], **params)
                    elif method == "z_score":
                        df[column] = normalizer.z_score_normalize(df[column], **params)
                    elif method == "log":
                        df[column] = normalizer.log_transform(df[column], **params)
                    elif method == "remove_outliers":
                        df = normalizer.remove_outliers(df, column, **params)
        
        # Convert results to list of dictionaries
        results = []
        if df is not None and not df.empty:
            # Convert DataFrame to list of dictionaries
            results = df.to_dict(orient="records")
            
            # Convert numpy types to Python native types
            for i, record in enumerate(results):
                for key, value in record.items():
                    if hasattr(value, "item"):
                        # Convert numpy types to Python native types
                        results[i][key] = value.item()
                    elif isinstance(value, datetime):
                        # Convert datetime to ISO format string
                        results[i][key] = value.isoformat()
        
        # Generate visualization if requested
        visualization_data = None
        if request.include_visualization and df is not None and not df.empty:
            visualizer = DataVisualizer()
            
            # Determine visualization type
            viz_type = request.visualization_type or ChartType.AUTO
            
            # Determine appropriate visualization based on data and requested type
            if viz_type == ChartType.AUTO:
                # Auto-detect best visualization
                time_dimension = AggregationDimension.TIME in dimensions
                num_dimensions = len(dimensions)
                num_metrics = len(request.metrics)
                
                if time_dimension and num_metrics >= 1:
                    viz_type = ChartType.LINE
                elif num_dimensions == 1 and num_metrics == 1:
                    viz_type = ChartType.BAR
                elif num_dimensions == 2 and num_metrics == 1:
                    viz_type = ChartType.HEATMAP
                elif num_dimensions == 1 and num_metrics > 1:
                    viz_type = ChartType.STACKED_BAR
                else:
                    viz_type = ChartType.TABLE
            
            # Create the appropriate visualization
            if viz_type == ChartType.LINE:
                # Determine x and y columns
                x_column = None
                for dimension in dimensions:
                    if dimension == AggregationDimension.TIME:
                        if time_granularity == TimeGranularity.DAY:
                            x_column = "date"
                        elif time_granularity == TimeGranularity.WEEK:
                            x_column = "week"
                        elif time_granularity == TimeGranularity.MONTH:
                            x_column = "month"
                        elif time_granularity == TimeGranularity.QUARTER:
                            x_column = "quarter"
                        elif time_granularity == TimeGranularity.YEAR:
                            x_column = "year"
                        break
                
                if not x_column and len(df.columns) > 0:
                    # Use the first non-metric column as x-axis
                    metric_columns = [metric.value.lower() for metric in request.metrics]
                    for col in df.columns:
                        if col.lower() not in metric_columns:
                            x_column = col
                            break
                
                y_columns = [metric.value.lower() for metric in request.metrics]
                
                if x_column and y_columns:
                    visualization_data = visualizer.create_line_chart(
                        df=df,
                        x_column=x_column,
                        y_columns=y_columns,
                        title="Custom Analytics",
                        x_label=x_column.capitalize(),
                        y_label="Value",
                        interactive=True,
                        output_format="json"
                    )
            
            elif viz_type == ChartType.BAR:
                # Determine x and y columns
                x_column = None
                for dimension in dimensions:
                    if dimension != AggregationDimension.TIME:
                        dimension_name = dimension.value.lower()
                        if dimension_name in df.columns:
                            x_column = dimension_name
                            break
                
                if not x_column and len(df.columns) > 0:
                    # Use the first non-metric column as x-axis
                    metric_columns = [metric.value.lower() for metric in request.metrics]
                    for col in df.columns:
                        if col.lower() not in metric_columns:
                            x_column = col
                            break
                
                y_column = request.metrics[0].value.lower() if request.metrics else None
                
                if x_column and y_column:
                    visualization_data = visualizer.create_bar_chart(
                        df=df,
                        x_column=x_column,
                        y_column=y_column,
                        title="Custom Analytics",
                        x_label=x_column.capitalize(),
                        y_label=y_column.capitalize(),
                        interactive=True,
                        output_format="json"
                    )
            
            elif viz_type == ChartType.STACKED_BAR:
                # Determine x and y columns
                x_column = None
                for dimension in dimensions:
                    dimension_name = dimension.value.lower()
                    if dimension_name in df.columns:
                        x_column = dimension_name
                        break
                
                if not x_column and len(df.columns) > 0:
                    # Use the first non-metric column as x-axis
                    metric_columns = [metric.value.lower() for metric in request.metrics]
                    for col in df.columns:
                        if col.lower() not in metric_columns:
                            x_column = col
                            break
                
                y_columns = [metric.value.lower() for metric in request.metrics]
                
                if x_column and y_columns:
                    visualization_data = visualizer.create_bar_chart(
                        df=df,
                        x_column=x_column,
                        y_columns=y_columns,
                        title="Custom Analytics",
                        x_label=x_column.capitalize(),
                        y_label="Value",
                        interactive=True,
                        output_format="json"
                    )
            
            elif viz_type == ChartType.PIE:
                # Determine label and value columns
                label_column = None
                for dimension in dimensions:
                    dimension_name = dimension.value.lower()
                    if dimension_name in df.columns:
                        label_column = dimension_name
                        break
                
                if not label_column and len(df.columns) > 0:
                    # Use the first non-metric column as label
                    metric_columns = [metric.value.lower() for metric in request.metrics]
                    for col in df.columns:
                        if col.lower() not in metric_columns:
                            label_column = col
                            break
                
                value_column = request.metrics[0].value.lower() if request.metrics else None
                
                if label_column and value_column:
                    visualization_data = visualizer.create_pie_chart(
                        df=df,
                        label_column=label_column,
                        value_column=value_column,
                        title="Custom Analytics",
                        interactive=True,
                        output_format="json"
                    )
            
            elif viz_type == ChartType.HEATMAP:
                # Determine x, y, and value columns
                x_column = None
                y_column = None
                
                # Try to identify two dimension columns for x and y
                dimension_columns = []
                for dimension in dimensions:
                    dimension_name = dimension.value.lower()
                    if dimension_name in df.columns:
                        dimension_columns.append(dimension_name)
                
                if len(dimension_columns) >= 2:
                    x_column = dimension_columns[0]
                    y_column = dimension_columns[1]
                
                value_column = request.metrics[0].value.lower() if request.metrics else None
                
                if x_column and y_column and value_column:
                    visualization_data = visualizer.create_heatmap(
                        df=df,
                        x_column=x_column,
                        y_column=y_column,
                        value_column=value_column,
                        title="Custom Analytics",
                        x_label=x_column.capitalize(),
                        y_label=y_column.capitalize(),
                        interactive=True,
                        output_format="json"
                    )
            
            elif viz_type == ChartType.SCATTER:
                # Need at least two metrics for scatter plot
                if len(request.metrics) >= 2:
                    x_column = request.metrics[0].value.lower()
                    y_column = request.metrics[1].value.lower()
                    
                    # Optional color dimension
                    color_column = None
                    if len(dimensions) > 0:
                        dimension_name = dimensions[0].value.lower()
                        if dimension_name in df.columns:
                            color_column = dimension_name
                    
                    visualization_data = visualizer.create_scatter_plot(
                        df=df,
                        x_column=x_column,
                        y_column=y_column,
                        color_column=color_column,
                        title="Custom Analytics",
                        x_label=x_column.capitalize(),
                        y_label=y_column.capitalize(),
                        interactive=True,
                        output_format="json"
                    )
            
            elif viz_type == ChartType.TABLE:
                # Just return the data in a table format
                visualization_data = {
                    "type": "table",
                    "data": results,
                    "columns": list(df.columns)
                }
        
        # Prepare metadata
        metadata = {
            "metrics": [metric.value for metric in request.metrics],
            "dimensions": [dim.dimension.value for dim in request.dimensions],
            "filters": {cond.field: {"operator": cond.operator, "value": cond.value} for cond in request.filters} if request.filters else {},
            "time_range": {
                "start_date": request.start_date.isoformat() if request.start_date else None,
                "end_date": request.end_date.isoformat() if request.end_date else None
            },
            "result_count": len(results),
            "visualization_type": viz_type.value if hasattr(viz_type, "value") else str(viz_type)
        }
        
        return CustomAnalyticsResponse(
            data=results,
            visualization=visualization_data,
            metadata=metadata
        )
    
    except Exception as e:
        logging.error(f"Error performing custom analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error performing custom analytics: {str(e)}")

@router.post("/correlation", response_model=Dict[str, Any])
async def get_correlation_analysis(
    metrics: List[AggregationMetric] = Body(...),
    dimension: Optional[AggregationDimension] = Body(None),
    start_date: Optional[datetime] = Body(None),
    end_date: Optional[datetime] = Body(None),
    filters: Optional[List[FilterCondition]] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Analyze correlation between different metrics.
    
    - **metrics**: List of metrics to analyze correlation between (at least 2)
    - **dimension**: Optional dimension to group by
    - **start_date**: Optional start date for the analysis
    - **end_date**: Optional end date for the analysis
    - **filters**: Optional filter conditions to apply to the data
    
    Returns correlation matrix and visualization.
    """
    try:
        if len(metrics) < 2:
            raise HTTPException(status_code=400, detail="At least 2 metrics are required for correlation analysis")
        
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Process dimensions
        dimensions = [dimension] if dimension else []
        
        # Process filters
        filter_dict = {}
        if filters:
            for filter_condition in filters:
                filter_dict[filter_condition.field] = {
                    "operator": filter_condition.operator,
                    "value": filter_condition.value
                }
        
        # Get data for correlation analysis
        df = aggregator.aggregate_ticket_metrics(
            metrics=metrics,
            dimensions=dimensions,
            start_date=start_date,
            end_date=end_date,
            filters=filter_dict
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found for correlation analysis")
        
        # Extract metric columns for correlation
        import pandas as pd
        import numpy as np
        
        metric_columns = [metric.value.lower() for metric in metrics]
        correlation_df = df[metric_columns].copy()
        
        # Calculate correlation matrix
        correlation_matrix = correlation_df.corr().round(3)
        
        # Convert correlation matrix to dictionary
        correlation_data = correlation_matrix.to_dict(orient="index")
        
        # Create visualization
        visualizer = DataVisualizer()
        
        # Create heatmap for correlation matrix
        viz_df = correlation_matrix.reset_index()
        viz_df = pd.melt(viz_df, id_vars="index", value_vars=metric_columns)
        viz_df.columns = ["x", "y", "value"]
        
        visualization = visualizer.create_heatmap(
            df=viz_df,
            x_column="x",
            y_column="y",
            value_column="value",
            title="Correlation Matrix",
            x_label="Metric",
            y_label="Metric",
            interactive=True,
            output_format="json",
            color_scale="RdBu_r"
        )
        
        return {
            "metrics": [metric.value for metric in metrics],
            "correlation_matrix": correlation_data,
            "visualization": visualization
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error performing correlation analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error performing correlation analysis: {str(e)}")

@router.post("/anomaly-detection", response_model=Dict[str, Any])
async def detect_anomalies(
    metric: AggregationMetric = Body(...),
    dimension: AggregationDimension = Body(...),
    start_date: Optional[datetime] = Body(None),
    end_date: Optional[datetime] = Body(None),
    sensitivity: float = Body(1.5, description="Z-score threshold for anomaly detection"),
    filters: Optional[List[FilterCondition]] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Detect anomalies in time series or dimensional data.
    
    - **metric**: Metric to analyze for anomalies
    - **dimension**: Dimension to group by
    - **start_date**: Optional start date for the analysis
    - **end_date**: Optional end date for the analysis
    - **sensitivity**: Z-score threshold for anomaly detection (default: 1.5)
    - **filters**: Optional filter conditions to apply to the data
    
    Returns list of detected anomalies and visualization.
    """
    try:
        # Initialize aggregator and normalizer
        aggregator = DataAggregator(db)
        normalizer = DataNormalizer()
        
        # Process filters
        filter_dict = {}
        if filters:
            for filter_condition in filters:
                filter_dict[filter_condition.field] = {
                    "operator": filter_condition.operator,
                    "value": filter_condition.value
                }
        
        # Get data for anomaly detection
        df = aggregator.aggregate_ticket_metrics(
            metrics=[metric],
            dimensions=[dimension],
            start_date=start_date,
            end_date=end_date,
            filters=filter_dict
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found for anomaly detection")
        
        # Determine dimension and metric columns
        dimension_column = dimension.value.lower()
        metric_column = metric.value.lower()
        
        if dimension_column not in df.columns or metric_column not in df.columns:
            raise HTTPException(status_code=400, detail="Invalid dimension or metric column")
        
        # Detect anomalies using Z-score
        df["z_score"] = normalizer.z_score_normalize(df[metric_column])
        df["is_anomaly"] = abs(df["z_score"]) > sensitivity
        
        # Extract anomalies
        anomalies_df = df[df["is_anomaly"]].copy()
        
        # Format results
        anomalies = []
        for _, row in anomalies_df.iterrows():
            anomaly = {
                "dimension_value": row[dimension_column],
                "metric_value": float(row[metric_column]),
                "z_score": float(row["z_score"]),
                "direction": "high" if row["z_score"] > 0 else "low"
            }
            anomalies.append(anomaly)
        
        # Create visualization
        visualizer = DataVisualizer()
        
        # Prepare data for visualization
        import pandas as pd
        
        df["anomaly"] = df["is_anomaly"].map({True: "Anomaly", False: "Normal"})
        
        # Create the visualization
        visualization = visualizer.create_scatter_plot(
            df=df,
            x_column=dimension_column,
            y_column=metric_column,
            color_column="anomaly",
            title=f"Anomaly Detection - {metric.value}",
            x_label=dimension_column.capitalize(),
            y_label=metric.value,
            interactive=True,
            output_format="json"
        )
        
        return {
            "metric": metric.value,
            "dimension": dimension.value,
            "anomalies": anomalies,
            "sensitivity": sensitivity,
            "total_points": len(df),
            "anomaly_count": len(anomalies),
            "visualization": visualization
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error performing anomaly detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error performing anomaly detection: {str(e)}")

@router.post("/pivot-table", response_model=Dict[str, Any])
async def create_pivot_table(
    row_dimension: AggregationDimension = Body(...),
    column_dimension: AggregationDimension = Body(...),
    value_metric: AggregationMetric = Body(...),
    aggregation_function: str = Body("sum", description="Function to aggregate values: sum, avg, min, max, count"),
    start_date: Optional[datetime] = Body(None),
    end_date: Optional[datetime] = Body(None),
    filters: Optional[List[FilterCondition]] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Create a pivot table from the data.
    
    - **row_dimension**: Dimension for pivot table rows
    - **column_dimension**: Dimension for pivot table columns
    - **value_metric**: Metric for pivot table values
    - **aggregation_function**: Function to aggregate values
    - **start_date**: Optional start date for the analysis
    - **end_date**: Optional end date for the analysis
    - **filters**: Optional filter conditions to apply to the data
    
    Returns pivot table data and visualization.
    """
    try:
        # Initialize aggregator
        aggregator = DataAggregator(db)
        
        # Process filters
        filter_dict = {}
        if filters:
            for filter_condition in filters:
                filter_dict[filter_condition.field] = {
                    "operator": filter_condition.operator,
                    "value": filter_condition.value
                }
        
        # Get data for pivot table
        df = aggregator.aggregate_ticket_metrics(
            metrics=[value_metric],
            dimensions=[row_dimension, column_dimension],
            start_date=start_date,
            end_date=end_date,
            filters=filter_dict
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found for pivot table")
        
        # Determine dimension and metric columns
        row_column = row_dimension.value.lower()
        column_column = column_dimension.value.lower()
        value_column = value_metric.value.lower()
        
        if row_column not in df.columns or column_column not in df.columns or value_column not in df.columns:
            raise HTTPException(status_code=400, detail="Invalid dimension or metric columns")
        
        # Create pivot table
        import pandas as pd
        
        # Map aggregation function
        agg_func = None
        if aggregation_function == "sum":
            agg_func = "sum"
        elif aggregation_function == "avg":
            agg_func = "mean"
        elif aggregation_function == "min":
            agg_func = "min"
        elif aggregation_function == "max":
            agg_func = "max"
        elif aggregation_function == "count":
            agg_func = "count"
        else:
            agg_func = "sum"
        
        pivot_df = pd.pivot_table(
            df,
            values=value_column,
            index=row_column,
            columns=column_column,
            aggfunc=agg_func,
            fill_value=0
        )
        
        # Convert pivot table to dictionary
        pivot_data = {
            "rows": pivot_df.index.tolist(),
            "columns": pivot_df.columns.tolist(),
            "data": pivot_df.values.tolist()
        }
        
        # Create visualization
        visualizer = DataVisualizer()
        
        # Create heatmap for pivot table
        # Reset index to convert to regular columns
        viz_df = pivot_df.reset_index()
        
        # Melt the dataframe to get it into a format suitable for heatmap
        id_vars = [row_column]
        value_vars = pivot_df.columns.tolist()
        
        melted_df = pd.melt(viz_df, id_vars=id_vars, value_vars=value_vars)
        melted_df.columns = ["row", "column", "value"]
        
        visualization = visualizer.create_heatmap(
            df=melted_df,
            x_column="column",
            y_column="row",
            value_column="value",
            title=f"Pivot Table - {value_metric.value}",
            x_label=column_dimension.value,
            y_label=row_dimension.value,
            interactive=True,
            output_format="json"
        )
        
        return {
            "row_dimension": row_dimension.value,
            "column_dimension": column_dimension.value,
            "value_metric": value_metric.value,
            "aggregation_function": aggregation_function,
            "pivot_table": pivot_data,
            "visualization": visualization
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating pivot table: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating pivot table: {str(e)}")