from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "notification_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.email", "app.tasks.telegram"]
)

# Set some Celery configurations
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# Optional: Define periodic tasks
celery_app.conf.beat_schedule = {
    # Example for a periodic task
    # 'send-daily-summary': {
    #     'task': 'app.tasks.email.send_daily_summary',
    #     'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
    # },
}

if __name__ == "__main__":
    celery_app.start()