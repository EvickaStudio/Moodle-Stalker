from abc import ABC, abstractmethod

from .chat import GPT


class BaseGPT(ABC):
    """Abstract base class for GPT implementations."""

    @abstractmethod
    def context_assistant(self, text: str) -> str:
        """Process text with context-aware assistant."""
        pass

    @abstractmethod
    def chat_completion(
        self,
        model: str,
        system_message: str,
        user_message: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Complete chat interaction."""
        pass


__all__ = ["GPT", "BaseGPT"]
