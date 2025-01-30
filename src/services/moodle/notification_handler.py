import logging
import time
from typing import Optional, TypedDict

from src.core.config import Config
from src.core.service_locator import ServiceLocator
from src.services.moodle.api import MoodleAPI

from .errors import MoodleAuthenticationError, MoodleConnectionError

logger = logging.getLogger(__name__)


class NotificationData(TypedDict):
    """Type definition for Moodle notification data."""

    id: int
    useridfrom: int
    subject: str
    fullmessagehtml: str


class UserData(TypedDict):
    """Type definition for Moodle user data."""

    id: int
    fullname: str
    profileimageurl: str


class MoodleNotificationHandler:
    """
    Handles fetching and processing of Moodle notifications.

    This class manages the connection to Moodle, authentication,
    and retrieval of notifications and user information.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize the notification handler.

        Args:
            config: Application configuration

        Raises:
            MoodleConnectionError: If connection to Moodle fails
            MoodleAuthenticationError: If authentication fails
            ValueError: If required configuration is missing
        """
        try:
            self.config = config
            self.api = ServiceLocator().get("moodle_api", MoodleAPI)
            self._login()

            # Get and store the authenticated user's ID
            self.moodle_user_id = self.api.get_user_id()
            if not self.moodle_user_id:
                raise MoodleAuthenticationError("Failed to get user ID after login")

            self.last_notification_id: Optional[int] = None

        except Exception as e:
            raise MoodleConnectionError(
                f"Failed to initialize Moodle connection: {str(e)}"
            ) from e

    def _login(self) -> None:
        """
        Authenticate with Moodle.

        Raises:
            MoodleAuthenticationError: If authentication fails
        """
        try:
            if not self.api.login(
                username=self.config.moodle.username,
                password=self.config.moodle.password,
            ):
                raise MoodleAuthenticationError("Login returned false")
            return None
        except Exception as e:
            raise MoodleAuthenticationError(f"Authentication failed: {str(e)}") from e

    def fetch_latest_notification(self) -> Optional[NotificationData]:
        """
        Fetch the most recent notification from Moodle.

        Returns:
            The latest notification if available, None otherwise

        Raises:
            MoodleConnectionError: If connection fails repeatedly
        """
        retry_delay = 60  # Initial delay in seconds
        max_delay = 300  # Maximum delay of 5 minutes
        max_retries = 5  # Maximum number of retries
        retries = 0

        while retries < max_retries:
            try:
                logger.info("Fetching notifications from Moodle")
                response = self.api.get_popup_notifications(self.moodle_user_id)

                if not isinstance(response, dict):
                    logger.error(f"Unexpected response type: {type(response)}")
                    return None

                notifications = response.get("notifications", [])
                if not notifications:
                    logger.info("No notifications found")
                    return None

                # Validate notification format
                notification = notifications[0]
                processed = self._process_notification(notification)
                if not processed:
                    logger.error("Failed to process notification")
                    return None

                logger.debug(f"Latest notification: {processed}")
                return processed

            except Exception as e:
                retries += 1
                if retries >= max_retries:
                    raise MoodleConnectionError(
                        f"Failed to fetch notifications after {max_retries} attempts"
                    ) from e

                logger.warning(
                    f"Failed to fetch notifications (attempt {retries}/{max_retries}): {str(e)}"
                )
                logger.info(f"Retrying in {retry_delay} seconds...")

                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_delay)  # Exponential backoff

        return None

    def fetch_newest_notification(self) -> Optional[NotificationData]:
        """
        Fetch only notifications newer than the last processed one.

        Returns:
            The newest unprocessed notification if available, None otherwise

        Raises:
            MoodleConnectionError: If fetching notifications fails
        """
        try:
            notification = self.fetch_latest_notification()
            if not notification:
                return None

            current_id = notification["id"]

            # First run or new notification
            if self.last_notification_id is None:
                return self._handle_new_notification(
                    "First notification fetched: ID ", current_id, notification
                )
            if current_id > self.last_notification_id:
                return self._handle_new_notification(
                    "New notification found: ID ", current_id, notification
                )
            logger.debug(
                f"No new notifications. Current ID: {current_id}, Last ID: {self.last_notification_id}"
            )
            return None

        except Exception as e:
            raise MoodleConnectionError(
                f"Failed to fetch new notifications: {str(e)}"
            ) from e

    def _handle_new_notification(
        self, message: str, current_id: int, notification: NotificationData
    ) -> NotificationData:
        """Handle processing of a new notification.

        Args:
            message: Log message prefix
            current_id: Current notification ID
            notification: Notification data

        Returns:
            The processed notification data
        """
        logger.info(f"{message}{current_id}")
        self.last_notification_id = current_id
        return notification

    def user_id_from(self, user_id: int) -> Optional[UserData]:
        """
        Fetch user information by ID.

        Args:
            user_id: The Moodle user ID to look up

        Returns:
            User information if found, None otherwise

        Raises:
            MoodleConnectionError: If the API call fails
        """
        try:
            logger.debug(f"Fetching user with ID {user_id}")
            response = self.api.core_user_get_users_by_field("id", str(user_id))

            if not response:
                logger.info(f"No user found with ID {user_id}")
                return None

            user_data = response[0]
            processed = self._process_user_data(user_data)
            if not processed:
                logger.error("Failed to process user data")
                return None

            logger.debug(f"User data fetched: {processed}")
            return processed

        except Exception as e:
            raise MoodleConnectionError(
                f"Failed to fetch user {user_id}: {str(e)}"
            ) from e

    def _process_notification(self, notification: dict) -> Optional[NotificationData]:
        """Process raw notification data into typed format."""
        try:
            # Validate all required fields are present
            required_fields = {"id", "useridfrom", "subject", "fullmessagehtml"}
            if any(field not in notification for field in required_fields):
                missing = required_fields - set(notification.keys())
                logging.error(f"Missing required notification fields: {missing}")
                return None

            # Create TypedDict with validated data
            return NotificationData(
                id=int(notification["id"]),
                useridfrom=int(notification["useridfrom"]),
                subject=str(notification["subject"]),
                fullmessagehtml=str(notification["fullmessagehtml"]),
            )
        except (KeyError, ValueError) as e:
            logging.error(f"Error processing notification data: {e}")
            return None

    def _process_user_data(self, user_data: dict) -> Optional[UserData]:
        """Process raw user data into typed format."""
        try:
            # Validate all required fields are present
            required_fields = {"id", "fullname", "profileimageurl"}
            if any(field not in user_data for field in required_fields):
                missing = required_fields - set(user_data.keys())
                logging.error(f"Missing required user fields: {missing}")
                return None

            # Create TypedDict with validated data
            return UserData(
                id=int(user_data["id"]),
                fullname=str(user_data["fullname"]),
                profileimageurl=str(user_data["profileimageurl"]),
            )
        except (KeyError, ValueError) as e:
            logging.error(f"Error processing user data: {e}")
            return None
