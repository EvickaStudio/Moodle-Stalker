from abc import ABC, abstractmethod
from typing import Optional


class NotificationProvider(ABC):
    """Base class for notification providers."""

    @abstractmethod
    def send(self, subject: str, message: str, summary: Optional[str] = None) -> bool:
        """Send a notification.

        Args:
            subject: Message subject/title
            message: Message content
            summary: Optional AI-generated summary

        Returns:
            bool: True if sent successfully, False otherwise
        """
        pass
