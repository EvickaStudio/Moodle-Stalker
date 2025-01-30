from unittest.mock import Mock, patch

import pytest

from core.notification.summarizer import NotificationSummarizer


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = Mock()
    config.get_summarize_enabled.return_value = True
    config.get_openai_api_key.return_value = "test-key"
    return config


def test_summarizer_initialization(mock_config):
    """Test summarizer initialization."""
    summarizer = NotificationSummarizer(mock_config)
    assert summarizer is not None


def test_summarize_with_empty_text(mock_config):
    """Test summarization with empty text."""
    summarizer = NotificationSummarizer(mock_config)
    assert summarizer.summarize("") == ""


def test_summarize_with_short_text(mock_config):
    """Test summarization with short text."""
    summarizer = NotificationSummarizer(mock_config)
    text = "This is a short text."
    assert summarizer.summarize(text) == ""


def test_summarize_with_long_text(mock_config):
    """Test summarization with long text."""
    summarizer = NotificationSummarizer(mock_config)
    text = "This is a very long text. " * 50
    with patch("src.gpt.deepinfra.GPT") as mock_gpt:
        mock_gpt.return_value.chat_completion.return_value = "Summary"
        assert summarizer.summarize(text) == "Summary"


def test_summarize_with_html_text(mock_config):
    """Test summarization with HTML text."""
    summarizer = NotificationSummarizer(mock_config)
    text = "<p>This is a very long text with HTML tags.</p> " * 50
    with patch("src.gpt.deepinfra.GPT") as mock_gpt:
        mock_gpt.return_value.chat_completion.return_value = "Summary"
        assert summarizer.summarize(text) == "Summary"


def test_summarize_with_api_error(mock_config):
    """Test summarization with API error."""
    summarizer = NotificationSummarizer(mock_config)
    text = "This is a very long text. " * 50
    with patch("src.gpt.deepinfra.GPT") as mock_gpt:
        mock_gpt.return_value.chat_completion.side_effect = Exception("API Error")
        assert summarizer.summarize(text) == ""


def test_summarize_disabled(mock_config):
    """Test summarization when disabled."""
    mock_config.get_summarize_enabled.return_value = False
    summarizer = NotificationSummarizer(mock_config)
    assert summarizer.summarize("Any text") == ""
