import logging
from typing import Optional

from src.core.notification.base import NotificationProvider

# from pushbullet import Pushbullet


logger = logging.getLogger(__name__)


class PushbulletProvider(NotificationProvider):
    """Pushbullet notification provider."""

    def __init__(self, api_key: str):
        # if not api_key:
        #     raise ValueError("Pushbullet API key is required")
        # self.pb = Pushbullet(api_key)
        return

    def send(self, subject: str, message: str, summary: Optional[str] = None) -> bool:
        # try:
        #     content = (
        #         f"{message}\n\nTLDR (AI Summary):\n{summary}" if summary else message
        #     )
        #     self.pb.push_note(subject, content)
        #     return True
        # except Exception as e:
        #     logger.error(f"Failed to send Pushbullet notification: {str(e)}")
        #     return False
        return True
