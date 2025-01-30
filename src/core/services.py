from src.core.config.loader import Config
from src.core.notification.processor import NotificationProcessor
from src.core.service_locator import ServiceLocator
from src.providers.notification import initialize_providers
from src.services.ai.chat import GPT
from src.services.moodle.api import MoodleAPI
from src.services.moodle.notification_handler import MoodleNotificationHandler


def initialize_services() -> None:
    """Initialize and register all application services."""
    # Initialize service locator
    locator = ServiceLocator()

    # Initialize config first as other services depend on it
    config = Config()
    locator.register("config", config)

    # Initialize Moodle API
    moodle_api = MoodleAPI(url=config.moodle.url)
    locator.register("moodle_api", moodle_api)

    # Initialize GPT if AI is enabled
    if config.ai.enabled:
        gpt = GPT()
        gpt.api_key = config.ai.api_key
        if config.ai.endpoint:
            gpt.endpoint = config.ai.endpoint
        locator.register("gpt", gpt)

    # Initialize notification providers and processor
    providers = initialize_providers(config)
    notification_processor = NotificationProcessor(config, providers)
    locator.register("notification_processor", notification_processor)

    # Initialize Moodle notification handler
    moodle_handler = MoodleNotificationHandler(config)
    locator.register("moodle_handler", moodle_handler)
