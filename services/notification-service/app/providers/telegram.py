import asyncio
from typing import Dict, Any, Optional

import telegram
from telegram.constants import ParseMode

from app.core.config import settings


class TelegramProvider:
    """Provider for sending messages via Telegram Bot API"""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.default_chat_id = settings.TELEGRAM_CHAT_ID
        self.bot = telegram.Bot(token=self.token)
    
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
        try:
            # Use default chat ID if none provided
            if not chat_id:
                chat_id = self.default_chat_id
                
            # Send message
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode
            )
            
            return {"status": "success"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Initialize provider
telegram_provider = TelegramProvider()