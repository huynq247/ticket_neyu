from fastapi import BackgroundTasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
import uuid
import pytz

from app.core.config import settings
from app.db.database import get_mongodb_client
from app.analytics.report_generator import generate_report_by_type
from app.analytics.report_exporter import export_report
from app.models.report import create_report
from app.models.notification import send_report_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create scheduler
scheduler = AsyncIOScheduler()

# Configure the scheduler
def configure_scheduler():
    """
    Configure the scheduler with MongoDB job store
    """
    try:
        # Get MongoDB client
        client = get_mongodb_client()
        db = client[settings.MONGODB_DATABASE]
        
        # Configure job stores
        jobstores = {
            'default': MongoDBJobStore(database=settings.MONGODB_DATABASE, 
                                      collection='scheduled_jobs',
                                      client=client)
        }
        
        # Configure executors
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        
        # Configure job defaults
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        
        # Configure scheduler
        scheduler.configure(jobstores=jobstores, 
                           executors=executors, 
                           job_defaults=job_defaults, 
                           timezone=pytz.utc)
        
        # Start the scheduler
        scheduler.start()
        logger.info("Scheduler started successfully")
        
    except Exception as e:
        logger.error(f"Error configuring scheduler: {str(e)}")
        raise


async def generate_and_save_report(
    report_type: str,
    params: Dict[str, Any],
    user_id: str,
    template_id: Optional[str] = None,
    export_formats: List[str] = ["json"],
    send_notification: bool = False,
    notification_email: Optional[str] = None
):
    """
    Generate a report, save it to the database, and optionally send notification
    """
    try:
        # Generate the report
        report_data = await generate_report_by_type(
            report_type=report_type,
            **params
        )
        
        if "error" in report_data:
            logger.error(f"Error generating report: {report_data['error']}")
            return None
        
        # Create exports
        exports = {}
        for export_format in export_formats:
            export_result = export_report(report_data, export_format)
            if "error" not in export_result:
                exports[export_format] = export_result
        
        # Save the report
        report = {
            "type": report_type,
            "name": f"{report_type.replace('_', ' ').title()} Report",
            "description": f"Automatically generated {report_type} report",
            "data": report_data,
            "params": params,
            "template_id": template_id,
            "exports": exports,
            "created_by": user_id,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to database
        saved_report = create_report(report)
        
        # Send notification if requested
        if send_notification and saved_report and notification_email:
            await send_report_notification(
                report_id=saved_report["id"],
                email=notification_email,
                report_name=saved_report["name"]
            )
        
        return saved_report
    
    except Exception as e:
        logger.error(f"Error in generate_and_save_report: {str(e)}")
        return None


def schedule_report(
    schedule_data: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Schedule a report to be generated periodically
    
    schedule_data should contain:
    - report_type: type of report to generate
    - params: parameters for the report
    - schedule: schedule information (frequency, start_date, etc.)
    - user_id: ID of the user scheduling the report
    - export_formats: list of export formats
    - send_notification: whether to send notification
    - notification_email: email to send notification to
    """
    try:
        report_type = schedule_data.get("report_type")
        params = schedule_data.get("params", {})
        user_id = schedule_data.get("user_id")
        template_id = schedule_data.get("template_id")
        export_formats = schedule_data.get("export_formats", ["json"])
        send_notification = schedule_data.get("send_notification", False)
        notification_email = schedule_data.get("notification_email")
        
        schedule_info = schedule_data.get("schedule", {})
        frequency = schedule_info.get("frequency", "daily")
        start_date = schedule_info.get("start_date")
        end_date = schedule_info.get("end_date")
        
        if not start_date:
            start_date = datetime.now() + timedelta(minutes=1)
        else:
            start_date = datetime.fromisoformat(start_date)
        
        if end_date:
            end_date = datetime.fromisoformat(end_date)
        
        # Generate a job ID
        job_id = str(uuid.uuid4())
        
        # Define the job function
        job_kwargs = {
            "report_type": report_type,
            "params": params,
            "user_id": user_id,
            "template_id": template_id,
            "export_formats": export_formats,
            "send_notification": send_notification,
            "notification_email": notification_email
        }
        
        # Schedule based on frequency
        if frequency == "one_time":
            # Schedule one-time job
            scheduler.add_job(
                generate_and_save_report,
                'date',
                run_date=start_date,
                kwargs=job_kwargs,
                id=job_id,
                replace_existing=True
            )
        elif frequency == "daily":
            # Schedule daily job
            scheduler.add_job(
                generate_and_save_report,
                'interval',
                days=1,
                start_date=start_date,
                end_date=end_date,
                kwargs=job_kwargs,
                id=job_id,
                replace_existing=True
            )
        elif frequency == "weekly":
            # Schedule weekly job
            scheduler.add_job(
                generate_and_save_report,
                'interval',
                weeks=1,
                start_date=start_date,
                end_date=end_date,
                kwargs=job_kwargs,
                id=job_id,
                replace_existing=True
            )
        elif frequency == "monthly":
            # Schedule monthly job
            scheduler.add_job(
                generate_and_save_report,
                'interval',
                days=30,  # Approximate month
                start_date=start_date,
                end_date=end_date,
                kwargs=job_kwargs,
                id=job_id,
                replace_existing=True
            )
        else:
            logger.error(f"Unsupported frequency: {frequency}")
            return {"error": f"Unsupported frequency: {frequency}"}
        
        # If this is a one-time job that should run now, also run it in the background
        if frequency == "one_time" and (start_date - datetime.now()).total_seconds() < 60:
            background_tasks.add_task(
                generate_and_save_report,
                **job_kwargs
            )
        
        # Return schedule information
        return {
            "job_id": job_id,
            "report_type": report_type,
            "frequency": frequency,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat() if end_date else None,
            "user_id": user_id
        }
    
    except Exception as e:
        logger.error(f"Error scheduling report: {str(e)}")
        return {"error": str(e)}


def cancel_scheduled_report(job_id: str) -> bool:
    """
    Cancel a scheduled report job
    """
    try:
        scheduler.remove_job(job_id)
        return True
    except Exception as e:
        logger.error(f"Error canceling scheduled report: {str(e)}")
        return False


def get_scheduled_report_jobs(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all scheduled report jobs for a user or all jobs if user_id is None
    """
    try:
        jobs = scheduler.get_jobs()
        job_list = []
        
        for job in jobs:
            job_kwargs = job.kwargs
            job_user_id = job_kwargs.get("user_id")
            
            # Filter by user_id if provided
            if user_id and job_user_id != user_id:
                continue
            
            # Extract job details
            job_info = {
                "job_id": job.id,
                "report_type": job_kwargs.get("report_type"),
                "params": job_kwargs.get("params"),
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "user_id": job_user_id
            }
            
            job_list.append(job_info)
        
        return job_list
    
    except Exception as e:
        logger.error(f"Error getting scheduled jobs: {str(e)}")
        return []