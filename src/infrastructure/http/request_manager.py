from typing import Optional

import requests

from src.core.version import __version__


class RequestManager:
    """Global request session manager with consistent headers."""

    _instance: Optional["RequestManager"] = None
    _session: Optional[requests.Session] = None

    def __new__(cls) -> "RequestManager":
        if cls._instance is None:
            cls._instance = super(RequestManager, cls).__new__(cls)
            cls._instance._setup_session()
        return cls._instance

    def _setup_session(self) -> None:
        """Setup the global session with default headers."""
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": f"MoodleMate/{__version__} (+https://github.com/EvickaStudio/Moodle-Mate)",
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

    @property
    def session(self) -> requests.Session:
        """Get the global session instance."""
        if self._session is None:
            self._setup_session()
        assert self._session is not None
        return self._session

    def update_headers(self, headers: dict) -> None:
        """Update session headers with new values."""
        if self._session is None:
            self._setup_session()
        assert self._session is not None
        self._session.headers.update(headers)


# Global instance
request_manager = RequestManager()
