import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
import logging

from app.models.sql_models import (
    FactTicket, DimDate, FactUserActivity
)
from app.schemas.analytics import (
    TimeGranularity, ForecastResult
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_forecast(
    db: Session,
    metric: str,
    start_date: datetime,
    end_date: datetime,
    periods: int,
    interval_width: float,
    granularity: TimeGranularity
) -> ForecastResult:
    """
    Generate forecast for a specific metric
    """
    # Get historical data
    history_df = get_historical_data(db, metric, start_date, end_date, granularity)
    
    if history_df.empty or len(history_df) < 3:
        raise ValueError(f"Insufficient historical data for forecasting {metric}")
    
    # Generate forecast
    forecast_df = forecast_time_series(history_df, periods, interval_width)
    
    # Format result
    result = ForecastResult(
        metric=metric,
        granularity=granularity,
        dates=[d.strftime("%Y-%m-%d") for d in forecast_df.index],
        forecast=forecast_df["forecast"].tolist(),
        lower_bound=forecast_df["lower_bound"].tolist(),
        upper_bound=forecast_df["upper_bound"].tolist()
    )
    
    return result

def get_historical_data(
    db: Session,
    metric: str,
    start_date: datetime,
    end_date: datetime,
    granularity: TimeGranularity
) -> pd.DataFrame:
    """
    Get historical data for a specific metric
    """
    data = []
    dates = []
    
    # Define date ranges based on granularity
    current_date = start_date
    while current_date <= end_date:
        # Calculate period end based on granularity
        if granularity == TimeGranularity.DAY:
            period_end = current_date.replace(hour=23, minute=59, second=59)
            next_date = current_date + timedelta(days=1)
        elif granularity == TimeGranularity.WEEK:
            period_end = current_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
            next_date = current_date + timedelta(weeks=1)
        elif granularity == TimeGranularity.MONTH:
            # Get last day of month
            if current_date.month == 12:
                period_end = current_date.replace(day=31, hour=23, minute=59, second=59)
            else:
                next_month = current_date.replace(month=current_date.month + 1)
                period_end = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)
            
            # Move to next month
            if current_date.month == 12:
                next_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                next_date = current_date.replace(month=current_date.month + 1)
        elif granularity == TimeGranularity.QUARTER:
            # Calculate quarter end
            quarter = (current_date.month - 1) // 3
            if quarter == 3:  # Q4
                period_end = current_date.replace(month=12, day=31, hour=23, minute=59, second=59)
            else:
                next_quarter_month = (quarter + 1) * 3 + 1
                next_quarter = current_date.replace(month=next_quarter_month)
                period_end = (next_quarter - timedelta(days=1)).replace(hour=23, minute=59, second=59)
            
            # Move to next quarter
            next_month = 3 * ((current_date.month - 1) // 3 + 1) + 1
            next_year = current_date.year
            if next_month > 12:
                next_month = 1
                next_year += 1
            next_date = current_date.replace(year=next_year, month=next_month, day=1)
        elif granularity == TimeGranularity.YEAR:
            period_end = current_date.replace(month=12, day=31, hour=23, minute=59, second=59)
            next_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
        
        # Ensure period_end is not after end_date
        if period_end > end_date:
            period_end = end_date
        
        # Get metric value for this period
        value = get_metric_value(db, metric, current_date, period_end)
        
        # Add to data
        data.append(value)
        dates.append(current_date)
        
        # Move to next period
        current_date = next_date
    
    # Create DataFrame
    df = pd.DataFrame({"value": data}, index=dates)
    return df

def get_metric_value(
    db: Session,
    metric: str,
    start_date: datetime,
    end_date: datetime
) -> float:
    """
    Get the value of a specific metric for a given period
    """
    if metric == "ticket_count":
        return db.query(FactTicket)\
            .join(DimDate, FactTicket.created_date_id == DimDate.id)\
            .filter(DimDate.date >= start_date, DimDate.date <= end_date)\
            .count()
    
    elif metric == "avg_response_time":
        avg_time = db.query(db.func.avg(FactTicket.response_time_minutes))\
            .join(DimDate, FactTicket.created_date_id == DimDate.id)\
            .filter(
                DimDate.date >= start_date,
                DimDate.date <= end_date,
                FactTicket.response_time_minutes.isnot(None)
            )\
            .scalar()
        
        return float(avg_time) if avg_time is not None else 0
    
    elif metric == "avg_resolution_time":
        avg_time = db.query(db.func.avg(FactTicket.resolution_time_minutes))\
            .join(DimDate, FactTicket.created_date_id == DimDate.id)\
            .filter(
                DimDate.date >= start_date,
                DimDate.date <= end_date,
                FactTicket.resolution_time_minutes.isnot(None)
            )\
            .scalar()
        
        return float(avg_time) if avg_time is not None else 0
    
    elif metric == "tickets_closed":
        return db.query(FactTicket)\
            .join(DimDate, FactTicket.resolved_date_id == DimDate.id)\
            .filter(DimDate.date >= start_date, DimDate.date <= end_date)\
            .count()
    
    elif metric == "user_activity":
        total_activity = db.query(db.func.sum(FactUserActivity.tickets_created + FactUserActivity.tickets_closed))\
            .join(DimDate, FactUserActivity.date_id == DimDate.id)\
            .filter(DimDate.date >= start_date, DimDate.date <= end_date)\
            .scalar()
        
        return float(total_activity) if total_activity is not None else 0
    
    else:
        logger.warning(f"Unknown metric: {metric}")
        return 0

def forecast_time_series(
    history_df: pd.DataFrame,
    periods: int,
    interval_width: float
) -> pd.DataFrame:
    """
    Forecast time series using appropriate model
    """
    # Check if we have enough data
    if len(history_df) < 3:
        raise ValueError("Insufficient data for forecasting (need at least 3 data points)")
    
    # Determine appropriate model based on data characteristics
    # For simplicity, we'll use Exponential Smoothing for most cases
    # In a real system, you'd want to do model selection based on the data
    
    try:
        # Try Exponential Smoothing first
        model = ExponentialSmoothing(
            history_df["value"],
            trend="add",
            seasonal=None,
            damped=True
        )
        fit_model = model.fit()
        
        # Generate forecast
        forecast = fit_model.forecast(periods)
        prediction_intervals = fit_model.get_prediction(start=len(history_df), end=len(history_df) + periods - 1)
        
        # Extract confidence intervals
        alpha = 1 - interval_width  # e.g., 0.95 -> alpha = 0.05
        lower = prediction_intervals.conf_int(alpha=alpha).iloc[:, 0]
        upper = prediction_intervals.conf_int(alpha=alpha).iloc[:, 1]
        
    except Exception as e:
        logger.warning(f"Error with Exponential Smoothing model: {str(e)}. Falling back to ARIMA.")
        
        # Fall back to ARIMA
        try:
            model = ARIMA(history_df["value"], order=(1, 1, 0))
            fit_model = model.fit()
            
            # Generate forecast
            forecast = fit_model.forecast(periods)
            prediction_intervals = fit_model.get_forecast(periods)
            
            # Extract confidence intervals
            lower = prediction_intervals.conf_int().iloc[:, 0]
            upper = prediction_intervals.conf_int().iloc[:, 1]
            
        except Exception as e2:
            logger.error(f"Error with ARIMA model: {str(e2)}. Using naive forecast.")
            
            # Fall back to naive forecast (last value)
            last_value = history_df["value"].iloc[-1]
            forecast = pd.Series([last_value] * periods)
            
            # Simple confidence interval
            std = history_df["value"].std() if len(history_df) > 1 else history_df["value"].iloc[0] * 0.1
            z = 1.96  # Approx 95% confidence
            lower = pd.Series([last_value - z * std] * periods)
            upper = pd.Series([last_value + z * std] * periods)
    
    # Generate future dates
    last_date = history_df.index[-1]
    date_diff = history_df.index[1] - history_df.index[0] if len(history_df) > 1 else timedelta(days=1)
    future_dates = [last_date + (i + 1) * date_diff for i in range(periods)]
    
    # Create forecast DataFrame
    forecast_df = pd.DataFrame({
        "forecast": forecast.values if hasattr(forecast, 'values') else forecast,
        "lower_bound": lower.values if hasattr(lower, 'values') else lower,
        "upper_bound": upper.values if hasattr(upper, 'values') else upper
    }, index=future_dates)
    
    # Ensure non-negative values for counts
    if "ticket_count" in str(history_df) or "tickets_closed" in str(history_df) or "user_activity" in str(history_df):
        forecast_df["forecast"] = forecast_df["forecast"].apply(lambda x: max(0, x))
        forecast_df["lower_bound"] = forecast_df["lower_bound"].apply(lambda x: max(0, x))
    
    return forecast_df