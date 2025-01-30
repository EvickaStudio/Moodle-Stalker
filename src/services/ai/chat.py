import logging
import re
from typing import Dict, List, Optional

import openai  # version 1.5
import tiktoken
from openai.types.chat import ChatCompletion

from .calculate import ModelPricing, ModelType
from .errors import ChatCompletionError, InvalidAPIKeyError, TokenizationError


class GPT:
    """
    Interface for the OpenAI API with improved error handling and type safety.

    This class provides a type-safe interface to OpenAI's API with proper
    error handling, token counting, and cost tracking.

    Attributes:
        PRICING: Mapping of model types to their pricing information
        api_key: The OpenAI API key (property with validation)
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GPT, cls).__new__(cls)
            cls._instance._init_gpt()
        return cls._instance

    def _init_gpt(self):
        """Initialize GPT instance."""
        self._api_key = None
        self._endpoint = None
        self.PRICING = {
            ModelType.GPT4.value: ModelPricing(2.50, 10.00),
            ModelType.GPT4_0806.value: ModelPricing(2.50, 10.00),
            ModelType.GPT4_0513.value: ModelPricing(5.00, 15.00),
            ModelType.GPT4_MINI.value: ModelPricing(0.150, 0.600),
            ModelType.GPT4_MINI_0718.value: ModelPricing(0.150, 0.600),
            ModelType.GPT35_TURBO.value: ModelPricing(0.50, 1.50),
            ModelType.O1.value: ModelPricing(15.00, 60.00),
            ModelType.O1_1217.value: ModelPricing(15.00, 60.00),
            ModelType.O1_PREVIEW.value: ModelPricing(15.00, 60.00),
            ModelType.O1_PREVIEW_0912.value: ModelPricing(15.00, 60.00),
            ModelType.O1_MINI.value: ModelPricing(3.00, 12.00),
            ModelType.O1_MINI_0912.value: ModelPricing(3.00, 12.00),
        }
        self._api_key_pattern = re.compile(r"^sk-[A-Za-z0-9_-]{48,}$")

    @property
    def api_key(self) -> Optional[str]:
        """Get the configured API key."""
        return self._api_key

    @api_key.setter
    def api_key(self, key: str) -> None:
        """
        Set and validate the API key.

        Args:
            key: The OpenAI API key to use

        Raises:
            InvalidAPIKeyError: If the key is empty or invalid
        """
        if not key:
            raise InvalidAPIKeyError("API key cannot be empty")

        if not self._api_key_pattern.match(key):
            raise InvalidAPIKeyError(
                "Invalid API key format. Expected format: 'sk-' followed by 48+ alphanumeric characters"
            )

        self._api_key = key
        openai.api_key = key

    def count_tokens(self, text: str, model: str = ModelType.GPT4_MINI.value) -> int:
        """
        Count tokens in text for a specific model.

        Args:
            text: The text to tokenize
            model: The model to use for tokenization

        Returns:
            Number of tokens in the text

        Raises:
            TokenizationError: If token counting fails
        """
        try:
            encoder = tiktoken.encoding_for_model(model)
            return len(encoder.encode(text))
        except Exception as e:
            raise TokenizationError(
                f"Failed to count tokens for model {model}: {str(e)}"
            ) from e

    def _validate_model(self, model: str) -> None:
        """
        Validate that a model is supported.

        Args:
            model: The model name to validate

        Raises:
            ValueError: If the model is not supported
        """
        if model not in self.PRICING:
            supported_models = ", ".join(self.PRICING.keys())
            raise ValueError(
                f"Model '{model}' not supported. Supported models: {supported_models}"
            )

    def chat_completion(
        self,
        model: str,
        system_message: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response using OpenAI's chat completion.

        This method handles the chat completion request with proper error handling
        and cost logging.

        Args:
            model: The model to use
            system_message: Context message for the AI
            user_message: The user's input message
            temperature: Controls randomness (0.0-2.0)
            max_tokens: Optional maximum tokens in response

        Returns:
            The generated response text

        Raises:
            ChatCompletionError: If the completion fails
            ValueError: If the model is not supported
        """
        self._validate_model(model)
        logging.info(f"Requesting chat completion using model: {model}")

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        try:
            return self._chat_completion(messages, model, temperature, max_tokens)
        except TokenizationError as e:
            raise ChatCompletionError(f"Token counting failed: {str(e)}") from e
        except Exception as e:
            raise ChatCompletionError(f"Chat completion failed: {str(e)}") from e

    def _chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: Optional[int],
    ) -> str:
        """
        Internal method to handle chat completion requests.

        Args:
            messages: List of message dictionaries
            model: Model identifier
            temperature: Temperature parameter
            max_tokens: Maximum tokens for response

        Returns:
            Generated response text

        Raises:
            ChatCompletionError: If completion fails
            TokenizationError: If token counting fails
        """
        # Count input tokens
        input_tokens = sum(
            self.count_tokens(msg["content"], model=model) for msg in messages
        )

        # Make the API call
        response: ChatCompletion = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Extract and validate response
        if not response.choices:
            raise ChatCompletionError("No completion choices returned")

        output_text = response.choices[0].message.content or ""
        output_tokens = self.count_tokens(output_text, model=model)

        # Calculate and log costs
        pricing = self.PRICING[model]
        input_cost, output_cost, total_cost = pricing.calculate_costs(
            input_tokens, output_tokens
        )

        logging.info(
            f"\n{'-'*40}\n"
            f"{'Model':<15}: {model}\n"
            f"{'Input Tokens':<15}: {input_tokens:,}\n"
            f"{'Output Tokens':<15}: {output_tokens:,}\n"
            f"{'Input Cost':<15}: ${input_cost:.6f}\n"
            f"{'Output Cost':<15}: ${output_cost:.6f}\n"
            f"{'Total Cost':<15}: ${total_cost:.6f}\n"
            f"{'-'*40}"
        )

        return output_text

    def context_assistant(self, prompt: str) -> str:
        """
        Generate a response using the assistant API.

        Note: This is a placeholder for future implementation.
        Currently returns an empty string as the feature is not implemented.

        Args:
            prompt: The input prompt

        Returns:
            Empty string (feature not implemented)
        """
        logging.warning("Assistant API support is not implemented")
        return ""
