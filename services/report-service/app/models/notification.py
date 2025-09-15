from typing import Dict, Any, Optional
import logging
import httpx
import json
from datetime import datetime

from app.core.config import settings
from app.api.deps import get_service_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
NOTIFICATION_SERVICE_URL = settings.NOTIFICATION_SERVICE_URL


async def send_report_notification(
    report_id: str,
    email: str,
    report_name: str
) -> bool:
    """
    Send a notification about a generated report via the notification service
    """
    try:
        # Prepare notification payload
        notification_data = {
            "recipient_email": email,
            "subject": f"Report Ready: {report_name}",
            "template_name": "report_notification",
            "template_data": {
                "report_name": report_name,
                "report_id": report_id,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "download_url": f"{settings.REPORT_SERVICE_URL}/api/reports/download/{report_id}",
                "service_name": "Report Service"
            }
        }
        
        # Get service token
        token = get_service_token()
        
        # Send notification
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = await client.post(
                f"{NOTIFICATION_SERVICE_URL}/api/notifications/email",
                headers=headers,
                content=json.dumps(notification_data)
            )
            
            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"Notification sent successfully for report {report_id}")
                return True
            else:
                logger.error(f"Failed to send notification: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return False


async def send_scheduled_report_notification(
    scheduled_report_id: str,
    report_id: str,
    email: str,
    report_name: str
) -> bool:
    """
    Send a notification about a scheduled report that was generated
    """
    try:
        # Prepare notification payload
        notification_data = {
            "recipient_email": email,
            "subject": f"Scheduled Report Ready: {report_name}",
            "template_name": "scheduled_report_notification",
            "template_data": {
                "report_name": report_name,
                "report_id": report_id,
                "scheduled_report_id": scheduled_report_id,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "download_url": f"{settings.REPORT_SERVICE_URL}/api/reports/download/{report_id}",
                "service_name": "Report Service"
            }
        }
        
        # Get service token
        token = get_service_token()
        
        # Send notification
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = await client.post(
                f"{NOTIFICATION_SERVICE_URL}/api/notifications/email",
                headers=headers,
                content=json.dumps(notification_data)
            )
            
            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"Notification sent successfully for scheduled report {scheduled_report_id}")
                return True
            else:
                logger.error(f"Failed to send notification: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return False