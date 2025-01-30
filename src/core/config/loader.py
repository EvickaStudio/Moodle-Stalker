import configparser
from pathlib import Path
from typing import Any

from .schema import (
    AIConfig,
    DiscordConfig,
    MoodleConfig,
    NotificationConfig,
    PushbulletConfig,
)


class Config:
    """Configuration manager for MoodleMate."""

    _instance = None

    def __new__(cls, config_path: str = "config.ini"):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._init_config(config_path)
        return cls._instance

    def _init_config(self, config_path: str):
        """Initialize configuration from file."""
        self.config = configparser.ConfigParser()
        if not Path(config_path).exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        self.config.read(config_path)

        # Initialize config sections
        self.moodle = self._load_moodle_config()
        self.ai = self._load_ai_config()
        self.notification = self._load_notification_config()
        self.pushbullet = self._load_pushbullet_config()
        self.discord = self._load_discord_config()

    def _get_config(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback to default."""
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def _get_bool(self, section: str, key: str, default: bool = False) -> bool:
        """Get boolean configuration value."""
        value = self._get_config(section, key, str(int(default)))
        return value.lower() in ("1", "true", "yes", "on")

    def _load_moodle_config(self) -> MoodleConfig:
        """Load Moodle configuration."""
        return MoodleConfig(
            url=self._get_config("moodle", "url", ""),
            username=self._get_config("moodle", "username", ""),
            password=self._get_config("moodle", "password", ""),
        )

    def _load_ai_config(self) -> AIConfig:
        """Load AI configuration."""
        return AIConfig(
            enabled=self._get_bool("ai", "enabled", True),
            api_key=self._get_config("ai", "api_key", ""),
            model=self._get_config("ai", "model", "gpt-4"),
            temperature=float(self._get_config("ai", "temperature", "0.7")),
            max_tokens=int(self._get_config("ai", "max_tokens", "150")),
            system_prompt=self._get_config(
                "ai",
                "system_prompt",
                "Summarize the message concisely with appropriate emojis, excluding links.",
            ),
            endpoint=self._get_config("ai", "endpoint", None),
        )

    def _load_notification_config(self) -> NotificationConfig:
        """Load notification configuration."""
        return NotificationConfig(
            max_retries=int(self._get_config("notification", "max_retries", "5")),
            fetch_interval=int(
                self._get_config("notification", "fetch_interval", "60")
            ),
        )

    def _load_pushbullet_config(self) -> PushbulletConfig:
        """Load Pushbullet configuration."""
        return PushbulletConfig(
            enabled=self._get_bool("pushbullet", "enabled", False),
            api_key=self._get_config("pushbullet", "api_key", ""),
        )

    def _load_discord_config(self) -> DiscordConfig:
        """Load Discord configuration."""
        return DiscordConfig(
            enabled=self._get_bool("discord", "enabled", False),
            webhook_url=self._get_config("discord", "webhook_url", ""),
            bot_name=self._get_config("discord", "bot_name", "MoodleMate"),
            thumbnail_url=self._get_config("discord", "thumbnail_url", ""),
        )
