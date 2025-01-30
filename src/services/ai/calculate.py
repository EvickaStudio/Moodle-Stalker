from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class ModelType(Enum):
    """Supported OpenAI model types."""

    GPT4 = "gpt-4o"
    GPT4_MINI = "gpt-4o-mini"
    GPT35_TURBO = "gpt-3.5-turbo"
    GPT4_0806 = "gpt-4o-2024-08-06"
    GPT4_0513 = "gpt-4o-2024-05-13"
    GPT4_MINI_0718 = "gpt-4o-mini-2024-07-18"
    O1 = "o1"
    O1_1217 = "o1-2024-12-17"
    O1_PREVIEW = "o1-preview"
    O1_PREVIEW_0912 = "o1-preview-2024-09-12"
    O1_MINI = "o1-mini"
    O1_MINI_0912 = "o1-mini-2024-09-12"


@dataclass
class ModelPricing:
    """Pricing information for a model."""

    input_cost_per_1m: float
    output_cost_per_1m: float

    def calculate_costs(
        self, input_tokens: int, output_tokens: int
    ) -> Tuple[float, float, float]:
        """Calculate costs for token usage."""
        input_cost = input_tokens * (self.input_cost_per_1m / 1_000_000)
        output_cost = output_tokens * (self.output_cost_per_1m / 1_000_000)
        return input_cost, output_cost, input_cost + output_cost
