import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional

from app.core.config import settings


class EmailProvider:
    """Provider for sending emails via SMTP"""
    
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_address = settings.EMAIL_FROM
    
    def send_email(
        self,
        to_addresses: List[str],
        subject: str,
        html_content: str,
        cc_addresses: Optional[List[str]] = None,
        bcc_addresses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send an email via SMTP
        
        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject
            html_content: HTML content of the email
            cc_addresses: List of CC email addresses
            bcc_addresses: List of BCC email addresses
            
        Returns:
            Dictionary with status and any error message
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_address
            message["To"] = ", ".join(to_addresses)
            
            if cc_addresses:
                message["Cc"] = ", ".join(cc_addresses)
                
            # Add HTML part
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Set up SMTP connection
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                
                # Build recipient list
                all_recipients = to_addresses.copy()
                if cc_addresses:
                    all_recipients.extend(cc_addresses)
                if bcc_addresses:
                    all_recipients.extend(bcc_addresses)
                    
                # Send email
                server.sendmail(
                    self.from_address,
                    all_recipients,
                    message.as_string()
                )
                
            return {"status": "success"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Initialize provider
email_provider = EmailProvider()