from unittest.mock import Mock, patch

import pytest

from services.notification.sender import NotificationSender


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = Mock()
    config.get_discord_enabled.return_value = True
    config.get_pushbullet_enabled.return_value = True
    config.get_discord_webhook.return_value = "webhook"
    config.get_pushbullet_token.return_value = "token"
    return config


@pytest.fixture
def mock_user_info_provider():
    """Create a mock user info provider."""
    provider = Mock()
    provider.user_id_from.return_value = {
        "id": 1,
        "fullname": "Test User",
        "profileimageurl": "test.jpg",
    }
    return provider


@pytest.fixture
def sender(mock_config, mock_user_info_provider):
    """Create a notification sender instance."""
    sender = NotificationSender(
        config=mock_config,
        bot_name="TestBot",
        thumbnail="thumb.jpg",
        user_info_provider=mock_user_info_provider,
    )
    return sender


def test_sender_initialization(mock_config):
    """Test sender initialization with various configurations."""
    with patch("src.modules.pushbullet.Pushbullet") as mock_pushbullet, patch(
        "src.modules.discord.Discord"
    ) as mock_discord:
        sender = NotificationSender(
            config=mock_config,
            bot_name="TestBot",
            thumbnail="thumb.jpg",
        )
        assert mock_pushbullet.called
        assert mock_discord.called
        assert sender is not None


def test_send_to_all_services(sender):
    """Test sending notification to all services."""
    notification = {
        "id": 1,
        "subject": "Test",
        "fullmessagehtml": "Test message",
        "useridfrom": 1,
    }
    sender.send(
        subject=notification["subject"],
        text=notification["fullmessagehtml"],
        summary="Test summary",
        useridfrom=notification["useridfrom"],
    )


def test_send_without_summary(sender):
    """Test sending notification without summary."""
    notification = {
        "id": 1,
        "subject": "Test",
        "fullmessagehtml": "Test message",
        "useridfrom": 1,
    }
    sender.send(
        subject=notification["subject"],
        text=notification["fullmessagehtml"],
        summary="",
        useridfrom=notification["useridfrom"],
    )


def test_send_with_service_failure(sender):
    """Test sending notification with service failure."""
    notification = {
        "id": 1,
        "subject": "Test",
        "fullmessagehtml": "Test message",
        "useridfrom": 1,
    }
    sender.pushbullet.send.side_effect = Exception("Test error")
    sender.send(
        subject=notification["subject"],
        text=notification["fullmessagehtml"],
        summary="Test summary",
        useridfrom=notification["useridfrom"],
    )


def test_send_simple(sender):
    """Test sending simple notification."""
    sender.send_simple("Test message")


def test_send_simple_without_discord(mock_config):
    """Test sending simple notification without Discord."""
    mock_config.get_discord_enabled.return_value = False
    sender = NotificationSender(
        config=mock_config, bot_name="TestBot", thumbnail="thumb.jpg"
    )
    sender.send_simple("Test message")


def test_user_info_handling(sender):
    """Test user info handling in notifications."""
    sender.send(
        subject="Test", text="Test message", summary="Test summary", useridfrom=1
    )


def test_notification_config_validation():
    """Test notification configuration validation."""
    config = Mock()
    config.get_discord_enabled.return_value = False
    config.get_pushbullet_enabled.return_value = False

    with pytest.raises(ValueError):
        NotificationSender(config=config, bot_name="TestBot", thumbnail="thumb.jpg")
