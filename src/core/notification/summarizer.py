import logging

from src.core.config.loader import Config
from src.services.ai import GPT


class NotificationSummarizer:
    """Summarizes notification content using AI."""

    def __init__(self, config: Config):
        """Initialize the summarizer.

        Args:
            config: Configuration instance
        """
        self.config = config.ai
        if not self.config.enabled:
            logging.info("AI summarization is disabled")
            return

        if not self.config.api_key:
            raise ValueError("AI API key is required for summarization")

        self.ai_provider = GPT()
        self.ai_provider.api_key = self.config.api_key
        if self.config.endpoint:
            self.ai_provider.endpoint = self.config.endpoint

    def summarize(self, text: str) -> str:
        """Summarize the given text.

        Args:
            text: The text to summarize

        Returns:
            The summarized text

        Raises:
            ValueError: If the input text is empty
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        if not self.config.enabled:
            return text

        try:
            # First try using context_assistant
            # summary = self.ai_provider.context_assistant(text)
            # if summary:
            #     return summary

            # Fallback to chat_completion
            summary = self.ai_provider.chat_completion(
                model=self.config.model,
                system_message=self.config.system_prompt,
                user_message=text,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            return summary
        except Exception as e:
            logging.error(f"Failed to summarize text: {str(e)}")
            raise
