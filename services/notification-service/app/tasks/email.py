from typing import Dict, Any, List, Optional
from datetime import datetime
from celery import shared_task
from bson import ObjectId

from app.core.celery_app import celery_app
from app.core.template_engine import template_engine
from app.models.notification import get_notification, update_notification
from app.models.template import get_template_by_name
from app.providers.email import email_provider
from app.schemas.notification import NotificationStatus


@shared_task(
    name="send_email_notification",
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def send_email_notification(self, notification_id: str) -> Dict[str, Any]:
    """
    Celery task to send an email notification
    
    Args:
        notification_id: ID of the notification to send
        
    Returns:
        Dictionary with status and any error message
    """
    try:
        # Get notification
        notification = get_notification(notification_id)
        if not notification:
            return {"status": "error", "message": "Notification not found"}
        
        # Get recipient email from User Service (TODO: implement API call)
        # For now, we'll assume recipient_id is the email address
        recipient_email = notification["recipient_id"]
        
        # Get template
        template_name = notification["template_name"]
        template_data = notification["template_data"]
        
        # Get subject
        subject = notification.get("subject")
        if not subject:
            template_doc = get_template_by_name(template_name)
            if template_doc:
                subject = template_doc.get("subject", "Notification")
            else:
                subject = "Notification"
        
        # Render template
        html_content = template_engine.render_template(template_name, template_data)
        if not html_content:
            # Update notification status to failed
            update_notification(
                notification_id=notification_id,
                update_data={
                    "status": NotificationStatus.FAILED,
                    "error_message": f"Template '{template_name}' not found"
                }
            )
            return {"status": "error", "message": f"Template '{template_name}' not found"}
        
        # Send email
        result = email_provider.send_email(
            to_addresses=[recipient_email],
            subject=subject,
            html_content=html_content
        )
        
        # Update notification status based on result
        if result["status"] == "success":
            update_notification(
                notification_id=notification_id,
                update_data={
                    "status": NotificationStatus.SENT,
                    "sent_at": datetime.utcnow()
                }
            )
            return {"status": "success"}
        else:
            # Retry if failed
            try:
                raise Exception(result["message"])
            except Exception as exc:
                # If max retries reached, mark as failed
                if self.request.retries >= self.max_retries:
                    update_notification(
                        notification_id=notification_id,
                        update_data={
                            "status": NotificationStatus.FAILED,
                            "error_message": result["message"]
                        }
                    )
                    return {"status": "error", "message": result["message"]}
                # Otherwise retry
                self.retry(exc=exc)
    
    except Exception as e:
        # Update notification status to failed on unexpected error
        update_notification(
            notification_id=notification_id,
            update_data={
                "status": NotificationStatus.FAILED,
                "error_message": str(e)
            }
        )
        return {"status": "error", "message": str(e)}