class MoodleError(Exception):
    """Base exception for Moodle-related errors."""

    pass


class MoodleConnectionError(MoodleError):
    """Raised when connection to Moodle fails."""

    pass


class MoodleAuthenticationError(MoodleError):
    """Raised when authentication to Moodle fails."""

    pass
