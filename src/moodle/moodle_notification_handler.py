import logging
import time  # Added import for sleep
from typing import Optional

from src.utils import Config

from .api import MoodleAPI

logger = logging.getLogger(__name__)


class MoodleNotificationHandler:
    """
    Handles the fetching of Moodle notifications for a specific user.
    """

    def __init__(self, config: Config):
        """
        Initializes the MoodleNotificationHandler by loading the configuration.
        """
        self.config = config
        self.last_notification_id: Optional[int] = None
        self.logged_in = False
        try:
            self.url = self._get_config_value("moodle", "MOODLE_URL")
            self.api = MoodleAPI(self.url)
            self.__login()
            self.moodle_user_id = self.api.get_user_id()
        except Exception as e:
            logger.exception(f"Initialization failed: {e}")
            raise

    def _get_config_value(self, section: str, key: str) -> str:
        """
        Retrieves a configuration value and raises an error if it is missing.
        """
        if value := self.config.get_config(section, key):
            return value
        else:
            raise ValueError(
                f"Configuration value '{key}' is missing in section '{section}'."
            )

    def __login(self) -> None:
        """
        Logs in to Moodle using the username and password.
        """
        if not self.logged_in:
            try:
                self.username = self._get_config_value(
                    "moodle", "MOODLE_USERNAME"
                )
                self.password = self._get_config_value(
                    "moodle", "MOODLE_PASSWORD"
                )
                if self.api.login(
                    username=self.username, password=self.password
                ):

                    self.logged_in = True
            except Exception as e:
                logger.exception(f"Failed to log in to Moodle: {e}")
                raise

    def fetch_latest_notification(self) -> Optional[dict]:
        """
        Fetches the latest notification from Moodle.
        """
        retry_delay = 60  # Initial wait time in seconds
        while True:
            try:
                logger.info("Fetching notifications from Moodle.")
                response = self.api.get_popup_notifications(self.moodle_user_id)
                if notifications := response.get("notifications", []):
                    logger.debug(
                        f"Latest notification fetched: {notifications[0]}"
                    )
                    return notifications[0]
                else:
                    logger.info("No notifications found.")
                    return None
            except Exception as e:
                logger.exception(f"Failed to fetch Moodle notifications: {e}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay += 2  # Increment wait time

    def fetch_newest_notification(self) -> Optional[dict]:
        """
        Fetches the newest notification from Moodle by comparing it with the last notification fetched.
        """
        retry_delay = 60  # Initial wait time in seconds
        while True:
            try:
                if notification := self.fetch_latest_notification():
                    notification_id = notification.get("id")
                    if notification_id is None:
                        logger.warning(
                            "Notification does not contain an 'id' field."
                        )
                        return None

                    if self.last_notification_id is None:
                        # First run; set last_notification_id
                        self.last_notification_id = notification_id
                        logger.info(
                            f"First notification fetched: ID {notification_id}"
                        )
                        return notification
                    elif notification_id > self.last_notification_id:
                        # New notification found
                        logger.info(
                            f"New notification found: ID {notification_id}"
                        )
                        self.last_notification_id = notification_id
                        return notification
                    else:
                        # No new notifications
                        logger.info(
                            f"No new notifications. Current ID: {notification_id}, Last ID: {self.last_notification_id}"
                        )
                        return None
                else:
                    logger.info("No notifications fetched.")
                    return None
            except Exception as e:
                logger.exception(
                    f"Failed to fetch the newest Moodle notification: {e}"
                )
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay += 2  # Increment wait time

    def user_id_from(self, useridfrom: int) -> Optional[dict]:
        """
        Fetches the user information from Moodle based on the user ID.
        """
        try:
            logger.debug(f"Fetching user with ID {useridfrom} from Moodle.")
            if response := self.api.core_user_get_users_by_field(
                "id", str(useridfrom)
            ):
                logger.debug(f"User data fetched: {response[0]}")
                return response[0]
            else:
                logger.info(f"No user found with ID {useridfrom}.")
                return None
        except Exception as e:
            logger.exception(
                f"Failed to fetch user {useridfrom} from Moodle: {e}"
            )
            return None
