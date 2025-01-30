"""Shared test fixtures and configuration."""

import logging
from typing import Generator
from unittest.mock import Mock

import pytest


@pytest.fixture(autouse=True)
def setup_logging() -> Generator[None, None, None]:
    """Configure logging for tests."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    yield
    logging.getLogger().handlers.clear()


@pytest.fixture
def mock_config() -> Mock:
    """Create a base mock configuration."""
    config = Mock()
    config.get_config.return_value = None  # Default to None
    return config
