import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, desc, asc, and_, or_
import logging
from datetime import datetime, timedelta

from app.models.sql_models import (
    FactTicket, DimTicketType, DimTicketStatus, DimDate, 
    DimUser, DimPriority, DimDepartment, FactUserActivity
)
from app.schemas.analytics import (
    AggregationWindow, TimeGranularity, 
    AggregationDimension, AggregationMetric
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataAggregator:
    """
    Advanced data aggregation component for analytics
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def aggregate_ticket_metrics(
        self,
        metrics: List[AggregationMetric],
        dimensions: List[AggregationDimension],
        start_date: datetime,
        end_date: datetime,
        filters: Optional[Dict[str, Any]] = None,
        time_granularity: Optional[TimeGranularity] = None,
        limit: int = 1000,
        sort_by: Optional[str] = None,
        sort_order: str = "desc"
    ) -> pd.DataFrame:
        """
        Aggregate ticket metrics based on specified dimensions and filters
        
        Args:
            metrics: List of metrics to aggregate (e.g., count, avg_response_time)
            dimensions: List of dimensions to group by (e.g., ticket_type, status, department)
            start_date: Start date for the aggregation window
            end_date: End date for the aggregation window
            filters: Optional filters to apply (e.g., {"priority": "high"})
            time_granularity: Optional time granularity for time-based aggregation
            limit: Maximum number of results to return
            sort_by: Column to sort by
            sort_order: Sort order (asc or desc)
            
        Returns:
            Pandas DataFrame with aggregated metrics
        """
        query = self.db.query()
        
        # Add dimensions to query
        select_columns = []
        group_by_columns = []
        
        # Process dimensions
        for dimension in dimensions:
            if dimension == AggregationDimension.TICKET_TYPE:
                query = query.join(DimTicketType, FactTicket.ticket_type_id == DimTicketType.id)
                select_columns.append(DimTicketType.type_name.label('ticket_type'))
                group_by_columns.append(DimTicketType.type_name)
                
            elif dimension == AggregationDimension.STATUS:
                query = query.join(DimTicketStatus, FactTicket.status_id == DimTicketStatus.id)
                select_columns.append(DimTicketStatus.status_name.label('status'))
                group_by_columns.append(DimTicketStatus.status_name)
                
            elif dimension == AggregationDimension.DEPARTMENT:
                query = query.join(DimDepartment, FactTicket.department_id == DimDepartment.id)
                select_columns.append(DimDepartment.department_name.label('department'))
                group_by_columns.append(DimDepartment.department_name)
                
            elif dimension == AggregationDimension.PRIORITY:
                query = query.join(DimPriority, FactTicket.priority_id == DimPriority.id)
                select_columns.append(DimPriority.priority_name.label('priority'))
                group_by_columns.append(DimPriority.priority_name)
                
            elif dimension == AggregationDimension.ASSIGNEE:
                query = query.join(DimUser, FactTicket.assignee_id == DimUser.id)
                select_columns.append(DimUser.username.label('assignee'))
                group_by_columns.append(DimUser.username)
                
            elif dimension == AggregationDimension.TIME:
                if not time_granularity:
                    time_granularity = TimeGranularity.DAY
                
                query = query.join(DimDate, FactTicket.created_date_id == DimDate.id)
                
                if time_granularity == TimeGranularity.DAY:
                    select_columns.append(DimDate.date.label('date'))
                    group_by_columns.append(DimDate.date)
                    
                elif time_granularity == TimeGranularity.WEEK:
                    select_columns.append(func.date_trunc('week', DimDate.date).label('week'))
                    group_by_columns.append(func.date_trunc('week', DimDate.date))
                    
                elif time_granularity == TimeGranularity.MONTH:
                    select_columns.append(func.date_trunc('month', DimDate.date).label('month'))
                    group_by_columns.append(func.date_trunc('month', DimDate.date))
                    
                elif time_granularity == TimeGranularity.QUARTER:
                    select_columns.append(func.date_trunc('quarter', DimDate.date).label('quarter'))
                    group_by_columns.append(func.date_trunc('quarter', DimDate.date))
                    
                elif time_granularity == TimeGranularity.YEAR:
                    select_columns.append(func.date_trunc('year', DimDate.date).label('year'))
                    group_by_columns.append(func.date_trunc('year', DimDate.date))
        
        # Process metrics
        for metric in metrics:
            if metric == AggregationMetric.TICKET_COUNT:
                select_columns.append(func.count(FactTicket.id).label('ticket_count'))
                
            elif metric == AggregationMetric.AVG_RESPONSE_TIME:
                select_columns.append(func.avg(FactTicket.response_time_minutes).label('avg_response_time'))
                
            elif metric == AggregationMetric.AVG_RESOLUTION_TIME:
                select_columns.append(func.avg(FactTicket.resolution_time_minutes).label('avg_resolution_time'))
                
            elif metric == AggregationMetric.TICKETS_RESOLVED:
                select_columns.append(func.sum(
                    func.case([(FactTicket.resolved_date_id.isnot(None), 1)], else_=0)
                ).label('tickets_resolved'))
                
            elif metric == AggregationMetric.RESOLUTION_RATE:
                # Complex metric: tickets resolved / total tickets
                select_columns.append(
                    (func.sum(func.case([(FactTicket.resolved_date_id.isnot(None), 1)], else_=0)) / 
                     func.count(FactTicket.id) * 100).label('resolution_rate')
                )
                
            elif metric == AggregationMetric.SLA_COMPLIANCE:
                # SLA compliance percentage
                select_columns.append(
                    (func.sum(func.case([(FactTicket.sla_compliant == True, 1)], else_=0)) / 
                     func.count(FactTicket.id) * 100).label('sla_compliance')
                )
        
        # Add date filter
        query = query.join(DimDate, FactTicket.created_date_id == DimDate.id)
        query = query.filter(DimDate.date >= start_date, DimDate.date <= end_date)
        
        # Add custom filters
        if filters:
            for key, value in filters.items():
                if key == 'priority':
                    query = query.join(DimPriority, FactTicket.priority_id == DimPriority.id)
                    query = query.filter(DimPriority.priority_name == value)
                    
                elif key == 'status':
                    query = query.join(DimTicketStatus, FactTicket.status_id == DimTicketStatus.id)
                    query = query.filter(DimTicketStatus.status_name == value)
                    
                elif key == 'ticket_type':
                    query = query.join(DimTicketType, FactTicket.ticket_type_id == DimTicketType.id)
                    query = query.filter(DimTicketType.type_name == value)
                    
                elif key == 'department':
                    query = query.join(DimDepartment, FactTicket.department_id == DimDepartment.id)
                    query = query.filter(DimDepartment.department_name == value)
                    
                elif key == 'assignee':
                    query = query.join(DimUser, FactTicket.assignee_id == DimUser.id)
                    query = query.filter(DimUser.username == value)
        
        # Finalize query
        query = query.select_from(FactTicket).with_entities(*select_columns)
        
        # Add group by
        if group_by_columns:
            query = query.group_by(*group_by_columns)
        
        # Add sorting
        if sort_by:
            if sort_order.lower() == 'asc':
                query = query.order_by(asc(sort_by))
            else:
                query = query.order_by(desc(sort_by))
        
        # Add limit
        query = query.limit(limit)
        
        # Execute query and convert to DataFrame
        results = query.all()
        df = pd.DataFrame([dict(row) for row in results])
        
        return df
    
    def aggregate_user_activity(
        self,
        metrics: List[str],
        dimensions: List[str],
        start_date: datetime,
        end_date: datetime,
        filters: Optional[Dict[str, Any]] = None,
        time_granularity: Optional[TimeGranularity] = None,
        limit: int = 1000,
        sort_by: Optional[str] = None,
        sort_order: str = "desc"
    ) -> pd.DataFrame:
        """
        Aggregate user activity metrics
        """
        query = self.db.query()
        
        # Add dimensions to query
        select_columns = []
        group_by_columns = []
        
        # Process dimensions
        for dimension in dimensions:
            if dimension == 'user':
                query = query.join(DimUser, FactUserActivity.user_id == DimUser.id)
                select_columns.append(DimUser.username.label('user'))
                group_by_columns.append(DimUser.username)
                
            elif dimension == 'department':
                query = query.join(DimUser, FactUserActivity.user_id == DimUser.id)
                query = query.join(DimDepartment, DimUser.department_id == DimDepartment.id)
                select_columns.append(DimDepartment.department_name.label('department'))
                group_by_columns.append(DimDepartment.department_name)
                
            elif dimension == 'time':
                if not time_granularity:
                    time_granularity = TimeGranularity.DAY
                
                query = query.join(DimDate, FactUserActivity.date_id == DimDate.id)
                
                if time_granularity == TimeGranularity.DAY:
                    select_columns.append(DimDate.date.label('date'))
                    group_by_columns.append(DimDate.date)
                    
                elif time_granularity == TimeGranularity.WEEK:
                    select_columns.append(func.date_trunc('week', DimDate.date).label('week'))
                    group_by_columns.append(func.date_trunc('week', DimDate.date))
                    
                elif time_granularity == TimeGranularity.MONTH:
                    select_columns.append(func.date_trunc('month', DimDate.date).label('month'))
                    group_by_columns.append(func.date_trunc('month', DimDate.date))
                    
                elif time_granularity == TimeGranularity.QUARTER:
                    select_columns.append(func.date_trunc('quarter', DimDate.date).label('quarter'))
                    group_by_columns.append(func.date_trunc('quarter', DimDate.date))
                    
                elif time_granularity == TimeGranularity.YEAR:
                    select_columns.append(func.date_trunc('year', DimDate.date).label('year'))
                    group_by_columns.append(func.date_trunc('year', DimDate.date))
        
        # Process metrics
        for metric in metrics:
            if metric == 'tickets_created':
                select_columns.append(func.sum(FactUserActivity.tickets_created).label('tickets_created'))
                
            elif metric == 'tickets_closed':
                select_columns.append(func.sum(FactUserActivity.tickets_closed).label('tickets_closed'))
                
            elif metric == 'tickets_assigned':
                select_columns.append(func.sum(FactUserActivity.tickets_assigned).label('tickets_assigned'))
                
            elif metric == 'avg_response_time':
                select_columns.append(func.avg(FactUserActivity.avg_response_time).label('avg_response_time'))
                
            elif metric == 'avg_resolution_time':
                select_columns.append(func.avg(FactUserActivity.avg_resolution_time).label('avg_resolution_time'))
                
            elif metric == 'sla_compliance':
                select_columns.append(
                    (func.sum(FactUserActivity.sla_compliant_tickets) / 
                     func.sum(FactUserActivity.tickets_closed) * 100).label('sla_compliance')
                )
                
            elif metric == 'productivity_score':
                # Productivity score formula:
                # (tickets_closed * 1.0 + tickets_created * 0.5) / (working_hours)
                select_columns.append(
                    ((func.sum(FactUserActivity.tickets_closed) * 1.0 + 
                      func.sum(FactUserActivity.tickets_created) * 0.5) / 
                     func.sum(FactUserActivity.working_hours)).label('productivity_score')
                )
        
        # Add date filter
        query = query.join(DimDate, FactUserActivity.date_id == DimDate.id)
        query = query.filter(DimDate.date >= start_date, DimDate.date <= end_date)
        
        # Add custom filters
        if filters:
            for key, value in filters.items():
                if key == 'user':
                    query = query.join(DimUser, FactUserActivity.user_id == DimUser.id)
                    query = query.filter(DimUser.username == value)
                    
                elif key == 'department':
                    query = query.join(DimUser, FactUserActivity.user_id == DimUser.id)
                    query = query.join(DimDepartment, DimUser.department_id == DimDepartment.id)
                    query = query.filter(DimDepartment.department_name == value)
        
        # Finalize query
        query = query.select_from(FactUserActivity).with_entities(*select_columns)
        
        # Add group by
        if group_by_columns:
            query = query.group_by(*group_by_columns)
        
        # Add sorting
        if sort_by:
            if sort_order.lower() == 'asc':
                query = query.order_by(asc(sort_by))
            else:
                query = query.order_by(desc(sort_by))
        
        # Add limit
        query = query.limit(limit)
        
        # Execute query and convert to DataFrame
        results = query.all()
        df = pd.DataFrame([dict(row) for row in results])
        
        return df
    
    def get_ticket_trends(
        self,
        start_date: datetime,
        end_date: datetime,
        granularity: TimeGranularity = TimeGranularity.DAY,
        metric: str = "count",
        filters: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Get ticket trends over time
        """
        # Determine granularity and time format
        if granularity == TimeGranularity.DAY:
            date_trunc_expr = func.date_trunc('day', DimDate.date)
            date_format = '%Y-%m-%d'
        elif granularity == TimeGranularity.WEEK:
            date_trunc_expr = func.date_trunc('week', DimDate.date)
            date_format = '%Y-%m-%d (Week)'
        elif granularity == TimeGranularity.MONTH:
            date_trunc_expr = func.date_trunc('month', DimDate.date)
            date_format = '%Y-%m'
        elif granularity == TimeGranularity.QUARTER:
            date_trunc_expr = func.date_trunc('quarter', DimDate.date)
            date_format = '%Y-Q%q'
        elif granularity == TimeGranularity.YEAR:
            date_trunc_expr = func.date_trunc('year', DimDate.date)
            date_format = '%Y'
        
        # Determine metric
        if metric == "count":
            value_expr = func.count(FactTicket.id)
        elif metric == "avg_response_time":
            value_expr = func.avg(FactTicket.response_time_minutes)
        elif metric == "avg_resolution_time":
            value_expr = func.avg(FactTicket.resolution_time_minutes)
        elif metric == "sla_compliance":
            value_expr = func.sum(func.case([(FactTicket.sla_compliant == True, 1)], else_=0)) / func.count(FactTicket.id) * 100
        
        # Build query
        query = self.db.query(
            date_trunc_expr.label('time_period'),
            value_expr.label('value')
        )
        
        # Join tables
        query = query.join(DimDate, FactTicket.created_date_id == DimDate.id)
        
        # Add date filter
        query = query.filter(DimDate.date >= start_date, DimDate.date <= end_date)
        
        # Add custom filters
        if filters:
            for key, value in filters.items():
                if key == 'priority':
                    query = query.join(DimPriority, FactTicket.priority_id == DimPriority.id)
                    query = query.filter(DimPriority.priority_name == value)
                    
                elif key == 'status':
                    query = query.join(DimTicketStatus, FactTicket.status_id == DimTicketStatus.id)
                    query = query.filter(DimTicketStatus.status_name == value)
                    
                elif key == 'ticket_type':
                    query = query.join(DimTicketType, FactTicket.ticket_type_id == DimTicketType.id)
                    query = query.filter(DimTicketType.type_name == value)
                    
                elif key == 'department':
                    query = query.join(DimDepartment, FactTicket.department_id == DimDepartment.id)
                    query = query.filter(DimDepartment.department_name == value)
                    
                elif key == 'assignee':
                    query = query.join(DimUser, FactTicket.assignee_id == DimUser.id)
                    query = query.filter(DimUser.username == value)
        
        # Group by time period
        query = query.group_by(date_trunc_expr).order_by(date_trunc_expr)
        
        # Execute query and convert to DataFrame
        results = query.all()
        df = pd.DataFrame([(row.time_period.strftime(date_format), row.value) for row in results],
                         columns=['time_period', 'value'])
        
        return df
    
    def get_top_performers(
        self,
        start_date: datetime,
        end_date: datetime,
        metric: str = "tickets_closed",
        limit: int = 10
    ) -> pd.DataFrame:
        """
        Get top performers based on specified metric
        """
        # Determine metric
        if metric == "tickets_closed":
            value_expr = func.sum(FactUserActivity.tickets_closed)
        elif metric == "tickets_created":
            value_expr = func.sum(FactUserActivity.tickets_created)
        elif metric == "tickets_assigned":
            value_expr = func.sum(FactUserActivity.tickets_assigned)
        elif metric == "avg_response_time":
            value_expr = func.avg(FactUserActivity.avg_response_time)
        elif metric == "avg_resolution_time":
            value_expr = func.avg(FactUserActivity.avg_resolution_time)
        elif metric == "sla_compliance":
            value_expr = func.sum(FactUserActivity.sla_compliant_tickets) / func.sum(FactUserActivity.tickets_closed) * 100
        elif metric == "productivity_score":
            value_expr = (func.sum(FactUserActivity.tickets_closed) * 1.0 + 
                          func.sum(FactUserActivity.tickets_created) * 0.5) / func.sum(FactUserActivity.working_hours)
        
        # Build query
        query = self.db.query(
            DimUser.username.label('user'),
            DimDepartment.department_name.label('department'),
            value_expr.label('value')
        )
        
        # Join tables
        query = query.join(DimUser, FactUserActivity.user_id == DimUser.id)
        query = query.join(DimDepartment, DimUser.department_id == DimDepartment.id)
        query = query.join(DimDate, FactUserActivity.date_id == DimDate.id)
        
        # Add date filter
        query = query.filter(DimDate.date >= start_date, DimDate.date <= end_date)
        
        # Group by user and department
        query = query.group_by(DimUser.username, DimDepartment.department_name)
        
        # Sort by value (descending for most metrics, ascending for time-based metrics)
        if metric in ["avg_response_time", "avg_resolution_time"]:
            query = query.order_by(asc('value'))
        else:
            query = query.order_by(desc('value'))
        
        # Limit results
        query = query.limit(limit)
        
        # Execute query and convert to DataFrame
        results = query.all()
        df = pd.DataFrame([dict(row) for row in results])
        
        return df
    
    def get_comparative_analysis(
        self,
        start_date: datetime,
        end_date: datetime,
        dimension: str = "department",
        metrics: List[str] = ["tickets_closed", "avg_resolution_time"],
        limit: int = 10
    ) -> pd.DataFrame:
        """
        Compare different entities (departments, users, etc.) across multiple metrics
        """
        # Build query
        select_columns = []
        group_by_columns = []
        
        # Add dimension column
        if dimension == "department":
            select_columns.append(DimDepartment.department_name.label('entity'))
            group_by_columns.append(DimDepartment.department_name)
            join_tables = lambda q: (
                q.join(DimUser, FactUserActivity.user_id == DimUser.id)
                 .join(DimDepartment, DimUser.department_id == DimDepartment.id)
            )
        elif dimension == "user":
            select_columns.append(DimUser.username.label('entity'))
            group_by_columns.append(DimUser.username)
            join_tables = lambda q: q.join(DimUser, FactUserActivity.user_id == DimUser.id)
        
        # Add metric columns
        for metric in metrics:
            if metric == "tickets_closed":
                select_columns.append(func.sum(FactUserActivity.tickets_closed).label('tickets_closed'))
                
            elif metric == "tickets_created":
                select_columns.append(func.sum(FactUserActivity.tickets_created).label('tickets_created'))
                
            elif metric == "tickets_assigned":
                select_columns.append(func.sum(FactUserActivity.tickets_assigned).label('tickets_assigned'))
                
            elif metric == "avg_response_time":
                select_columns.append(func.avg(FactUserActivity.avg_response_time).label('avg_response_time'))
                
            elif metric == "avg_resolution_time":
                select_columns.append(func.avg(FactUserActivity.avg_resolution_time).label('avg_resolution_time'))
                
            elif metric == "sla_compliance":
                select_columns.append(
                    (func.sum(FactUserActivity.sla_compliant_tickets) / 
                     func.sum(FactUserActivity.tickets_closed) * 100).label('sla_compliance')
                )
                
            elif metric == "productivity_score":
                select_columns.append(
                    ((func.sum(FactUserActivity.tickets_closed) * 1.0 + 
                      func.sum(FactUserActivity.tickets_created) * 0.5) / 
                     func.sum(FactUserActivity.working_hours)).label('productivity_score')
                )
        
        # Build query
        query = self.db.query(*select_columns)
        
        # Join tables
        query = join_tables(query)
        query = query.join(DimDate, FactUserActivity.date_id == DimDate.id)
        
        # Add date filter
        query = query.filter(DimDate.date >= start_date, DimDate.date <= end_date)
        
        # Group by dimension
        query = query.group_by(*group_by_columns)
        
        # Limit results
        query = query.limit(limit)
        
        # Execute query and convert to DataFrame
        results = query.all()
        df = pd.DataFrame([dict(row) for row in results])
        
        return df