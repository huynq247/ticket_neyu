import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta
import pytz

from app.core.config import settings, DATABASE_URL
from app.etl.pipeline import run_daily_etl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create scheduler
scheduler = AsyncIOScheduler()

def configure_scheduler():
    """
    Configure the scheduler with job stores, executors, etc.
    """
    try:
        # Configure job stores
        jobstores = {
            'default': SQLAlchemyJobStore(url=DATABASE_URL)
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
        scheduler.configure(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=pytz.utc
        )
        
        # Schedule jobs
        schedule_etl_jobs()
        
        # Start the scheduler
        scheduler.start()
        logger.info("Scheduler started successfully")
        
    except Exception as e:
        logger.error(f"Error configuring scheduler: {str(e)}")
        raise

def schedule_etl_jobs():
    """
    Schedule ETL jobs
    """
    # Schedule daily ETL job to run at 2 AM UTC
    scheduler.add_job(
        run_daily_etl,
        'cron',
        hour=2,
        minute=0,
        id='daily_etl_job',
        replace_existing=True,
        name='Daily ETL Job'
    )
    
    logger.info("ETL jobs scheduled successfully")

async def run_one_time_etl(days: int = 30):
    """
    Run a one-time ETL job to load historical data
    """
    logger.info(f"Starting one-time ETL job to load {days} days of historical data")
    
    from app.db.database import get_db
    from app.etl.pipeline import ETLPipeline
    
    db = next(get_db())
    pipeline = ETLPipeline(db)
    
    try:
        await pipeline.run_etl_pipeline(days=days)
        logger.info("One-time ETL job completed")
    except Exception as e:
        logger.error(f"Error in one-time ETL job: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # This can be used to run the scheduler manually
    configure_scheduler()
    
    # Keep the main thread alive
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass