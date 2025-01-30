from configparser import ConfigParser

import pytest

from core.config.loader import Config


@pytest.fixture
def config_parser():
    """Create a mock config parser."""
    parser = ConfigParser()
    parser.add_section("test")
    parser.set("test", "key", "value")
    return parser


def test_config_initialization():
    """Test config initialization."""
    config = Config()
    assert isinstance(config.parser, ConfigParser)


def test_get_config():
    """Test getting config values."""
    config = Config()
    config.parser.add_section("test")
    config.parser.set("test", "key", "value")
    assert config.get_config("test", "key") == "value"


def test_get_config_with_default():
    """Test getting config values with default."""
    config = Config()
    assert config.get_config("test", "nonexistent", "default") == "default"


def test_get_config_boolean():
    """Test getting boolean config values."""
    config = Config()
    config.parser.add_section("test")
    config.parser.set("test", "true_value", "1")
    config.parser.set("test", "false_value", "0")
    assert config.get_config_boolean("test", "true_value") is True
    assert config.get_config_boolean("test", "false_value") is False


def test_get_config_boolean_with_default():
    """Test getting boolean config values with default."""
    config = Config()
    assert config.get_config_boolean("test", "nonexistent", True) is True


def test_get_config_int():
    """Test getting integer config values."""
    config = Config()
    config.parser.add_section("test")
    config.parser.set("test", "number", "42")
    assert config.get_config_int("test", "number") == 42


def test_get_config_int_with_default():
    """Test getting integer config values with default."""
    config = Config()
    assert config.get_config_int("test", "nonexistent", 42) == 42


def test_get_config_float():
    """Test getting float config values."""
    config = Config()
    config.parser.add_section("test")
    config.parser.set("test", "number", "3.14")
    assert config.get_config_float("test", "number") == 3.14


def test_get_config_float_with_default():
    """Test getting float config values with default."""
    config = Config()
    assert config.get_config_float("test", "nonexistent", 3.14) == 3.14
