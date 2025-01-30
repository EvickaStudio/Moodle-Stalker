from unittest.mock import Mock

import pytest

from core.notification.processor import NotificationProcessor


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = Mock()
    config.get_discord_enabled.return_value = True
    config.get_pushbullet_enabled.return_value = True
    config.get_summarize_enabled.return_value = True
    return config


@pytest.fixture
def processor(mock_config):
    """Create a notification processor instance."""
    return NotificationProcessor(mock_config)


def test_process_notification_with_summary(processor):
    """Test processing a notification with summary enabled."""
    notification = {"id": 1, "subject": "Test", "fullmessagehtml": "Test message"}
    processor.process_notification(notification)


def test_process_notification_without_summary(processor):
    """Test processing a notification without summary."""
    processor.config.get_summarize_enabled.return_value = False
    notification = {"id": 1, "subject": "Test", "fullmessagehtml": "Test message"}
    processor.process_notification(notification)


def test_process_notification_with_empty_message(processor):
    """Test processing a notification with empty message."""
    notification = {"id": 1, "subject": "Test", "fullmessagehtml": ""}
    processor.process_notification(notification)


def test_process_notification_with_none_message(processor):
    """Test processing a notification with None message."""
    notification = {"id": 1, "subject": "Test", "fullmessagehtml": None}
    processor.process_notification(notification)


def test_process_notification_with_html_message(processor):
    """Test processing a notification with HTML message."""
    notification = {"id": 1, "subject": "Test", "fullmessagehtml": "<p>Test</p>"}
    processor.process_notification(notification)


def test_process_notification_with_long_message(processor):
    """Test processing a notification with long message."""
    notification = {"id": 1, "subject": "Test", "fullmessagehtml": "Test " * 100}
    processor.process_notification(notification)


def test_process_notification_with_special_chars(processor):
    """Test processing a notification with special characters."""
    notification = {"id": 1, "subject": "Test", "fullmessagehtml": "Test & < > \" '"}
    processor.process_notification(notification)


def test_process_notification_with_multiple_paragraphs(processor):
    """Test processing a notification with multiple paragraphs."""
    notification = {"id": 1, "subject": "Test", "fullmessagehtml": "<p>P1</p><p>P2</p>"}
    processor.process_notification(notification)


def test_process_notification_with_links(processor):
    """Test processing a notification with links."""
    notification = {
        "id": 1,
        "subject": "Test",
        "fullmessagehtml": '<a href="test">Test</a>',
    }
    processor.process_notification(notification)


def test_process_notification_with_images(processor):
    """Test processing a notification with images."""
    notification = {
        "id": 1,
        "subject": "Test",
        "fullmessagehtml": '<img src="test.jpg">',
    }
    processor.process_notification(notification)
