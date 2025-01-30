import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

from src.core.notification.base import NotificationProvider
from src.core.version import __version__
from src.infrastructure.http.request_manager import request_manager

logger = logging.getLogger(__name__)


class DiscordWebhookEmbed:
    """Helper class to construct Discord embeds."""

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description[:2000]  # Discord limit
        self.fields: List[Dict[str, Union[str, bool]]] = []
        self.color = 0x5865F2  # Discord Blurple
        self.thumbnail: Optional[Dict[str, str]] = None
        self.footer: Optional[Dict[str, str]] = None
        self.timestamp: Optional[str] = None

    def add_field(
        self, name: str, value: str, inline: bool = False
    ) -> "DiscordWebhookEmbed":
        """Add a field to the embed."""
        if len(self.fields) < 25:  # Discord's limit
            self.fields.append(
                {
                    "name": name[:256],  # Discord limit
                    "value": value[:1024],  # Discord limit
                    "inline": inline,
                }
            )
        return self

    def set_color(self, hex_color: int) -> "DiscordWebhookEmbed":
        """Set the embed color using hex color."""
        self.color = hex_color
        return self

    def set_thumbnail(self, url: str) -> "DiscordWebhookEmbed":
        """Set the thumbnail image."""
        self.thumbnail = {"url": url}
        return self

    def set_footer(
        self, text: str, icon_url: Optional[str] = None
    ) -> "DiscordWebhookEmbed":
        """Set the footer content."""
        self.footer = {"text": text[:2048]}  # Discord limit
        if icon_url:
            self.footer["icon_url"] = icon_url
        return self

    def set_timestamp(
        self, timestamp: Optional[datetime] = None
    ) -> "DiscordWebhookEmbed":
        """Set ISO8601 timestamp."""
        self.timestamp = (
            timestamp.isoformat() if timestamp else datetime.utcnow().isoformat()
        )
        return self

    def to_dict(self) -> Dict:
        """Convert embed to dictionary format."""
        embed_dict = {
            "title": self.title,
            "description": self.description,
            "color": self.color,
        }

        if self.fields:
            embed_dict["fields"] = self.fields
        if self.thumbnail:
            embed_dict["thumbnail"] = self.thumbnail
        if self.footer:
            embed_dict["footer"] = self.footer
        if self.timestamp:
            embed_dict["timestamp"] = self.timestamp

        return embed_dict


class DiscordProvider(NotificationProvider):
    """Discord notification provider with rich embed support."""

    LOGO_URL = "https://raw.githubusercontent.com/EvickaStudio/Moodle-Mate/main/assets/logo.png"

    def __init__(self, webhook_url: str, bot_name: str, thumbnail_url: str) -> None:
        """Initialize Discord webhook provider.

        Args:
            webhook_url: Discord webhook URL
            bot_name: Name to display for the webhook bot
            thumbnail_url: URL for the thumbnail image
        """
        self.webhook_url = webhook_url
        self.bot_name = bot_name
        self.thumbnail_url = thumbnail_url
        self.session = request_manager.session

    def create_notification_embed(
        self, subject: str, content: str, summary: Optional[str] = None
    ) -> DiscordWebhookEmbed:
        """Create a formatted embed for the notification."""
        embed = DiscordWebhookEmbed(subject, content)

        # Set basic embed properties
        embed.set_color(0x5865F2)  # Discord Blurple
        embed.set_timestamp()

        if self.thumbnail_url:
            embed.set_thumbnail(self.thumbnail_url)

        # Add summary if provided
        if summary:
            embed.add_field("Summary", summary, inline=False)

        # Set footer with version info
        embed.set_footer(f"Moodle-Mate v{__version__}", icon_url=self.LOGO_URL)

        return embed

    def send(self, subject: str, content: str, summary: Optional[str] = None) -> bool:
        """Send a notification via Discord webhook.

        Args:
            subject: Notification subject/title
            content: Main notification content
            summary: Optional summary text

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create the webhook payload
            payload = {
                "username": self.bot_name,
                "avatar_url": self.LOGO_URL,
                "embeds": [
                    self.create_notification_embed(subject, content, summary).to_dict()
                ],
            }

            # Send the webhook request
            request_manager.update_headers({"Content-Type": "application/json"})
            response = self.session.post(self.webhook_url, json=payload)

            if response.status_code == 204:
                logger.info("Successfully sent Discord notification")
                return True

            logger.error(
                "Discord API returned unexpected status code: %d, Response: %s",
                response.status_code,
                response.text,
            )
            return False

        except Exception as e:
            logger.error("Failed to send Discord message: %s", str(e))
            return False
