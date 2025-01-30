import logging
from typing import Optional

from src.core.notification.base import NotificationProvider
from src.infrastructure.http.request_manager import request_manager

logger = logging.getLogger(__name__)


class NtfyProvider(NotificationProvider):
    """Ntfy notification provider."""

    def __init__(self, server_url: str, topic: str):
        if not server_url or not topic:
            raise ValueError("Ntfy server URL and topic are required")

        self.server_url = server_url.rstrip("/")
        self.topic = topic
        self.session = request_manager.session

    def send(self, subject: str, message: str, summary: Optional[str] = None) -> bool:
        try:
            url = f"{self.server_url}/{self.topic}"

            content = f"{summary}\n\nFull message:\n{message}" if summary else message
            request_manager.update_headers(
                {"Title": subject, "Priority": "default", "Tags": "moodle"}
            )

            response = self.session.post(url, data=content)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to send Ntfy notification: {str(e)}")
            return False
