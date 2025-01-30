from dataclasses import dataclass
from typing import Optional


@dataclass
class MoodleConfig:
    url: str
    username: str
    password: str


@dataclass
class AIConfig:
    enabled: bool = True
    api_key: str = ""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 150
    system_prompt: str = (
        "Summarize the message concisely with appropriate emojis, excluding links."
    )
    endpoint: Optional[str] = None


@dataclass
class NotificationConfig:
    max_retries: int = 5
    fetch_interval: int = 60


@dataclass
class PushbulletConfig:
    enabled: bool = False
    api_key: str = ""


@dataclass
class DiscordConfig:
    enabled: bool = False
    webhook_url: str = ""
    bot_name: str = "MoodleMate"
    thumbnail_url: str = ""
