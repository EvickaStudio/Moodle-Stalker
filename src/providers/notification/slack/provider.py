import logging
from typing import Optional

import requests

from src.core.notification.base import NotificationProvider

logger = logging.getLogger(__name__)


class SlackProvider(NotificationProvider):
    """Slack notification provider."""

    def __init__(self, webhook_url: str):
        if not webhook_url:
            raise ValueError("Slack webhook URL is required")
        self.webhook_url = webhook_url

    def send(self, subject: str, message: str, summary: Optional[str] = None) -> bool:
        try:
            content = f"*{subject}*\n{message}"
            if summary:
                content += f"\n\n*TLDR (AI Summary):*\n{summary}"

            response = requests.post(self.webhook_url, json={"text": content})
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {str(e)}")
            return False
