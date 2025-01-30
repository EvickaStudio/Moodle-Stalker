import logging
import os
from typing import Optional

from requests.exceptions import RequestException

from src.infrastructure.http.request_manager import request_manager

logger = logging.getLogger(__name__)


class MoodleAPI:
    """
    A simple Moodle API wrapper for Python.
    """

    _instance = None

    def __new__(cls, url: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(MoodleAPI, cls).__new__(cls)
            cls._instance._init_api(url)
        return cls._instance

    def _init_api(self, url: Optional[str] = None):
        """Initialize the API with URL and session."""
        self.url = url or os.getenv("MOODLE_URL")
        self.session = request_manager.session
        request_manager.update_headers(
            {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        self.token = None
        self.userid = None

    def login(self, username: str, password: str) -> bool:
        """
        Logs in to the Moodle instance using the provided username and password.
        """
        if not username:
            raise ValueError("Username is required")
        if not password:
            raise ValueError("Password is required")

        login_data = {
            "username": username,
            "password": password,
            "service": "moodle_mobile_app",
        }

        try:
            response = self.session.post(f"{self.url}/login/token.php", data=login_data)
            response.raise_for_status()

            if "token" in response.json():
                self.token = response.json()["token"]
                logger.info("Login successful")
                return True

            logger.error("Login failed: Invalid credentials")
            return False

        except RequestException as e:
            logger.error("Request to Moodle failed: %s", e)
            return False

    def get_site_info(self) -> Optional[dict]:
        """
        Retrieves site information from the Moodle instance.
        """
        if self.token is None:
            logger.error("Token not set. Please login first.")
            return None

        wsfunction = "core_webservice_get_site_info"
        params = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "moodlewsrestformat": "json",
        }

        try:
            response = self.session.post(
                f"{self.url}/webservice/rest/server.php", params=params
            )
            response.raise_for_status()
            self.userid = response.json().get("userid")
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to get site info: {e}")
            return None

    def get_user_id(self) -> Optional[int]:
        """
        Retrieve the user ID.
        """
        if self.token is None:
            logger.error("Token not set. Please login first.")
            return None

        result = self.get_site_info()
        return result["userid"] if result else None

    def get_popup_notifications(self, user_id: int) -> Optional[dict]:
        """
        Retrieves popup notifications for a user.
        """
        return self._post("message_popup_get_popup_notifications", user_id)

    def core_user_get_users_by_field(self, field: str, value: str) -> Optional[dict]:
        """
        Retrieves user info based on a specific field and value.
        """
        if self.token is None:
            logger.error("Token not set. Please login first.")
            return None

        wsfunction = "core_user_get_users_by_field"
        params = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "field": field,
            "values[0]": value,
            "moodlewsrestformat": "json",
        }

        try:
            response = self.session.post(
                f"{self.url}/webservice/rest/server.php", params=params
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to get user by field: {e}")
            return None

    def _post(self, wsfunction: str, user_id: int) -> Optional[dict]:
        """
        Sends a POST request to the Moodle API with the given wsfunction and user ID.
        """
        if self.token is None:
            logger.error("Token not set. Please login first.")
            return None

        params = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "useridto": user_id,
            "moodlewsrestformat": "json",
        }

        try:
            response = self.session.post(
                f"{self.url}/webservice/rest/server.php", params=params
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(f"Request to Moodle failed: {e}")
            return None
