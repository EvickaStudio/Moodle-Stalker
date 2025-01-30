class OpenAIError(Exception):
    """Base exception for OpenAI-related errors."""

    pass


class InvalidAPIKeyError(OpenAIError):
    """Raised when the API key is invalid."""

    pass


class TokenizationError(OpenAIError):
    """Raised when token counting fails."""

    pass


class ChatCompletionError(OpenAIError):
    """Raised when chat completion fails."""

    pass
