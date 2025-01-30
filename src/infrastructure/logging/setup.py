import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ANSI color codes
COLORS = {
    "DEBUG": "\033[36m",  # Cyan
    "INFO": "\033[32m",  # Green
    "WARNING": "\033[33m",  # Yellow
    "ERROR": "\033[31m",  # Red
    "CRITICAL": "\033[41m",  # Red background
    "RESET": "\033[0m",  # Reset color
}


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages."""

    def format(self, record):
        # Save original levelname
        orig_levelname = record.levelname
        # Add color to levelname
        record.levelname = (
            f"{COLORS.get(record.levelname, '')}{record.levelname}{COLORS['RESET']}"
        )

        # Color the logger name/component
        if record.name != "root":
            record.name = f"\033[35m{record.name}\033[0m"  # Magenta for component names

        # Format the message
        result = super().format(record)

        # Restore original levelname
        record.levelname = orig_levelname
        return result


def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging configuration.

    Args:
        log_level: The logging level to use (default: INFO)
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure logging format with more context
    log_format = (
        "%(asctime)s [%(levelname)s] [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    # Create colored formatter for console output
    console_formatter = ColoredFormatter(log_format, date_format)
    # Create plain formatter for file output (without colors)
    file_formatter = logging.Formatter(log_format, date_format)

    # Set up handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    file_handler = RotatingFileHandler(
        filename=log_dir / "moodlemate.log",
        encoding="utf-8",
        maxBytes=10 * 1024 * 1024,  # 10MB max file size
        backupCount=5,  # Keep 5 backup files
        mode="a",
    )
    file_handler.setFormatter(file_formatter)

    # Configure root logger
    logging.basicConfig(level=log_level, handlers=[console_handler, file_handler])

    # Set log level for specific loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
