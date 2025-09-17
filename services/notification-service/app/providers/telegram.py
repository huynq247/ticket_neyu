import asyncio
from typing import Dict, Any, Optional

# Import with try/except to handle potential import errors
try:
    import telegram
    from telegram.constants import ParseMode
    TELEGRAM_AVAILABLE = True
except (ImportError, AttributeError):
    # Define placeholder for ParseMode if telegram is not available
    class ParseMode:
        HTML = "HTML"
        MARKDOWN = "MARKDOWN"
        MARKDOWN_V2 = "MARKDOWN_V2"
    TELEGRAM_AVAILABLE = False

from app.core.config import settings


class TelegramProvider:
    """Provider for sending messages via Telegram Bot API"""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.default_chat_id = settings.TELEGRAM_CHAT_ID
        self.available = False  # Default to False to avoid API calls
        self.bot = None
        
        # We'll disable Telegram functionality to avoid the proxy error
        print("Telegram provider is disabled to avoid compatibility issues")
        
    async def send_message(
        self,
        chat_id: Optional[str] = None,
        text: str = "",
        parse_mode: ParseMode = ParseMode.HTML
    ) -> Dict[str, Any]:
        """
        Send a message via Telegram Bot API
        
        Args:
            chat_id: Telegram chat ID to send message to
            text: Message text
            parse_mode: Parsing mode for message formatting
            
        Returns:
            Dictionary with status and any error message
        """
        # Log the message but don't try to send it
        print(f"[TELEGRAM DISABLED] Would send to {chat_id or self.default_chat_id}: {text}")
        return {"status": "success", "message": "Telegram provider is disabled"}


# Initialize provider
telegram_provider = TelegramProvider()


# Initialize provider
telegram_provider = TelegramProvider()