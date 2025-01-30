from typing import List

from src.core.config.loader import Config
from src.core.notification.base import NotificationProvider

from .discord.provider import DiscordProvider
from .ntfy.provider import NtfyProvider
from .pushbullet.provider import PushbulletProvider
from .slack.provider import SlackProvider


def initialize_providers(config: Config) -> List[NotificationProvider]:
    """Initialize enabled notification providers from config."""
    providers = []

    if config.discord.enabled:
        providers.append(
            DiscordProvider(
                webhook_url=config.discord.webhook_url,
                bot_name=config.discord.bot_name,
                thumbnail_url=config.discord.thumbnail_url,
            )
        )

    if config.pushbullet.enabled:
        providers.append(PushbulletProvider(api_key=config.pushbullet.api_key))

    # Add other providers as needed...

    return providers


__all__ = [
    "DiscordProvider",
    "PushbulletProvider",
    "SlackProvider",
    "NtfyProvider",
    "initialize_providers",
]
