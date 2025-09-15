import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple
import json
import os
from datetime import datetime, timedelta
import logging
from io import BytesIO
import base64

from app.core.config import settings
from app.api.deps import get_service_token
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TICKET_SERVICE_URL = settings.TICKET_SERVICE_URL
USER_SERVICE_URL = settings.USER_SERVICE_URL


async def fetch_data_from_service(endpoint: str, service_url: str) -> Dict[str, Any]:
    """
    Fetch data from another microservice using service token
    """
    try:
        token = get_service_token()
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{service_url}{endpoint}", headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching data from {service_url}{endpoint}: {str(e)}")
        return {"error": str(e)}


async def get_ticket_data(days: int = 30) -> pd.DataFrame:
    """
    Get ticket data from the ticket service
    """
    from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    endpoint = f"/api/tickets?from_date={from_date}&limit=1000"
    data = await fetch_data_from_service(endpoint, TICKET_SERVICE_URL)
    
    if "error" in data:
        logger.error(f"Failed to get ticket data: {data['error']}")
        return pd.DataFrame()
    
    tickets = data.get("tickets", [])
    return pd.DataFrame(tickets)


async def get_user_data() -> pd.DataFrame:
    """
    Get user data from the user service
    """
    endpoint = "/api/users?limit=1000"
    data = await fetch_data_from_service(endpoint, USER_SERVICE_URL)
    
    if "error" in data:
        logger.error(f"Failed to get user data: {data['error']}")
        return pd.DataFrame()
    
    users = data.get("users", [])
    return pd.DataFrame(users)


def plot_to_base64(fig) -> str:
    """
    Convert matplotlib figure to base64 string
    """
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str


async def generate_ticket_summary_report(days: int = 30) -> Dict[str, Any]:
    """
    Generate a summary report of ticket data
    """
    ticket_df = await get_ticket_data(days)
    
    if ticket_df.empty:
        return {
            "error": "No ticket data available",
            "timestamp": datetime.now().isoformat()
        }
    
    # Calculate summary statistics
    total_tickets = len(ticket_df)
    
    # Status breakdown
    status_counts = ticket_df['status'].value_counts().to_dict()
    
    # Priority breakdown
    priority_counts = ticket_df['priority'].value_counts().to_dict()
    
    # Calculate average resolution time
    if 'created_at' in ticket_df.columns and 'resolved_at' in ticket_df.columns:
        # Convert to datetime
        ticket_df['created_at'] = pd.to_datetime(ticket_df['created_at'])
        ticket_df['resolved_at'] = pd.to_datetime(ticket_df['resolved_at'])
        
        # Calculate only for resolved tickets
        resolved_tickets = ticket_df.dropna(subset=['resolved_at'])
        if not resolved_tickets.empty:
            resolution_times = (resolved_tickets['resolved_at'] - resolved_tickets['created_at'])
            avg_resolution_time = resolution_times.mean().total_seconds() / 3600  # in hours
        else:
            avg_resolution_time = None
    else:
        avg_resolution_time = None
    
    # Create visualizations
    charts = {}
    
    # Status chart
    if status_counts:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%')
        ax.set_title('Ticket Status Distribution')
        charts['status_distribution'] = plot_to_base64(fig)
    
    # Priority chart
    if priority_counts:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=list(priority_counts.keys()), y=list(priority_counts.values()), ax=ax)
        ax.set_title('Ticket Priority Distribution')
        ax.set_xlabel('Priority')
        ax.set_ylabel('Count')
        charts['priority_distribution'] = plot_to_base64(fig)
    
    # Daily ticket volume
    if 'created_at' in ticket_df.columns:
        ticket_df['date'] = ticket_df['created_at'].dt.date
        daily_counts = ticket_df.groupby('date').size()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        daily_counts.plot(kind='line', ax=ax)
        ax.set_title('Daily Ticket Volume')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Tickets')
        charts['daily_volume'] = plot_to_base64(fig)
    
    # Create report data
    report_data = {
        "summary": {
            "total_tickets": total_tickets,
            "status_distribution": status_counts,
            "priority_distribution": priority_counts,
            "avg_resolution_time_hours": avg_resolution_time
        },
        "charts": charts,
        "timestamp": datetime.now().isoformat(),
        "period_days": days
    }
    
    return report_data


async def generate_user_activity_report(days: int = 30) -> Dict[str, Any]:
    """
    Generate a report of user activity
    """
    ticket_df = await get_ticket_data(days)
    user_df = await get_user_data()
    
    if ticket_df.empty or user_df.empty:
        return {
            "error": "No data available",
            "timestamp": datetime.now().isoformat()
        }
    
    # Merge user data with ticket data
    if 'created_by' in ticket_df.columns and 'id' in user_df.columns:
        # Rename user id to avoid collision
        user_df = user_df.rename(columns={'id': 'user_id'})
        
        # Merge on created_by = user_id
        merged_df = pd.merge(
            ticket_df, 
            user_df, 
            left_on='created_by', 
            right_on='user_id',
            how='left'
        )
    else:
        return {
            "error": "Required columns missing in data",
            "timestamp": datetime.now().isoformat()
        }
    
    # Calculate user activity metrics
    tickets_per_user = merged_df.groupby('created_by').size().reset_index(name='ticket_count')
    if 'role' in user_df.columns:
        role_activity = merged_df.groupby('role').size().reset_index(name='ticket_count')
    else:
        role_activity = None
    
    # Create visualizations
    charts = {}
    
    # Top 10 most active users
    top_users = tickets_per_user.sort_values('ticket_count', ascending=False).head(10)
    if not top_users.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='ticket_count', y='created_by', data=top_users, ax=ax)
        ax.set_title('Top 10 Most Active Users')
        ax.set_xlabel('Number of Tickets')
        ax.set_ylabel('User ID')
        charts['top_users'] = plot_to_base64(fig)
    
    # Role-based activity
    if role_activity is not None and not role_activity.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x='role', y='ticket_count', data=role_activity, ax=ax)
        ax.set_title('Ticket Creation by User Role')
        ax.set_xlabel('Role')
        ax.set_ylabel('Number of Tickets')
        charts['role_activity'] = plot_to_base64(fig)
    
    # Create report data
    report_data = {
        "summary": {
            "total_users": len(user_df),
            "active_users": len(tickets_per_user),
            "tickets_per_user_avg": tickets_per_user['ticket_count'].mean() if not tickets_per_user.empty else 0,
            "most_active_user": {
                "id": top_users.iloc[0]['created_by'] if not top_users.empty else None,
                "ticket_count": top_users.iloc[0]['ticket_count'] if not top_users.empty else 0
            }
        },
        "charts": charts,
        "timestamp": datetime.now().isoformat(),
        "period_days": days
    }
    
    return report_data


async def generate_response_time_report(days: int = 30) -> Dict[str, Any]:
    """
    Generate a report analyzing response times for tickets
    """
    ticket_df = await get_ticket_data(days)
    
    if ticket_df.empty:
        return {
            "error": "No ticket data available",
            "timestamp": datetime.now().isoformat()
        }
    
    # Check if required columns exist
    required_cols = ['created_at', 'first_response_at', 'resolved_at', 'priority']
    if not all(col in ticket_df.columns for col in required_cols):
        missing_cols = [col for col in required_cols if col not in ticket_df.columns]
        return {
            "error": f"Required columns missing: {missing_cols}",
            "timestamp": datetime.now().isoformat()
        }
    
    # Convert datetime columns
    for col in ['created_at', 'first_response_at', 'resolved_at']:
        ticket_df[col] = pd.to_datetime(ticket_df[col])
    
    # Calculate response times
    ticket_df['first_response_time'] = (ticket_df['first_response_at'] - ticket_df['created_at']).dt.total_seconds() / 3600  # hours
    ticket_df['resolution_time'] = (ticket_df['resolved_at'] - ticket_df['created_at']).dt.total_seconds() / 3600  # hours
    
    # Filter out invalid entries
    response_df = ticket_df.dropna(subset=['first_response_time']).copy()
    resolution_df = ticket_df.dropna(subset=['resolution_time']).copy()
    
    # Calculate summary statistics
    avg_first_response = response_df['first_response_time'].mean() if not response_df.empty else None
    avg_resolution = resolution_df['resolution_time'].mean() if not resolution_df.empty else None
    
    # Response time by priority
    response_by_priority = response_df.groupby('priority')['first_response_time'].mean().to_dict() if not response_df.empty else {}
    resolution_by_priority = resolution_df.groupby('priority')['resolution_time'].mean().to_dict() if not resolution_df.empty else {}
    
    # Create visualizations
    charts = {}
    
    # Response time distribution
    if not response_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(response_df['first_response_time'], bins=20, kde=True, ax=ax)
        ax.set_title('First Response Time Distribution (Hours)')
        ax.set_xlabel('Hours')
        ax.set_ylabel('Frequency')
        charts['response_distribution'] = plot_to_base64(fig)
    
    # Resolution time distribution
    if not resolution_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(resolution_df['resolution_time'], bins=20, kde=True, ax=ax)
        ax.set_title('Resolution Time Distribution (Hours)')
        ax.set_xlabel('Hours')
        ax.set_ylabel('Frequency')
        charts['resolution_distribution'] = plot_to_base64(fig)
    
    # Response time by priority
    if response_by_priority:
        fig, ax = plt.subplots(figsize=(8, 6))
        priorities = list(response_by_priority.keys())
        times = list(response_by_priority.values())
        sns.barplot(x=priorities, y=times, ax=ax)
        ax.set_title('Average First Response Time by Priority (Hours)')
        ax.set_xlabel('Priority')
        ax.set_ylabel('Hours')
        charts['response_by_priority'] = plot_to_base64(fig)
    
    # Resolution time by priority
    if resolution_by_priority:
        fig, ax = plt.subplots(figsize=(8, 6))
        priorities = list(resolution_by_priority.keys())
        times = list(resolution_by_priority.values())
        sns.barplot(x=priorities, y=times, ax=ax)
        ax.set_title('Average Resolution Time by Priority (Hours)')
        ax.set_xlabel('Priority')
        ax.set_ylabel('Hours')
        charts['resolution_by_priority'] = plot_to_base64(fig)
    
    # Create report data
    report_data = {
        "summary": {
            "avg_first_response_time_hours": avg_first_response,
            "avg_resolution_time_hours": avg_resolution,
            "response_by_priority": response_by_priority,
            "resolution_by_priority": resolution_by_priority
        },
        "charts": charts,
        "timestamp": datetime.now().isoformat(),
        "period_days": days
    }
    
    return report_data


# Additional report generators can be added here
async def generate_report_by_type(report_type: str, days: int = 30, **params) -> Dict[str, Any]:
    """
    Generate a report based on the specified type
    """
    report_generators = {
        "ticket_summary": generate_ticket_summary_report,
        "user_activity": generate_user_activity_report,
        "response_time": generate_response_time_report,
        # Add more report types here
    }
    
    if report_type not in report_generators:
        return {
            "error": f"Unknown report type: {report_type}",
            "timestamp": datetime.now().isoformat()
        }
    
    return await report_generators[report_type](days=days, **params)