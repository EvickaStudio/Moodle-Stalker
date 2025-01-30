import argparse
import logging
import sys
import time

from src.core.config.generator import ConfigGenerator
from src.core.config.loader import Config
from src.core.notification.processor import NotificationProcessor
from src.core.service_locator import ServiceLocator
from src.core.services import initialize_services
from src.core.utils.retry import with_retry
from src.infrastructure.logging.setup import setup_logging
from src.services.moodle.notification_handler import MoodleNotificationHandler
from src.ui.cli.screen import animate_logo, logo_lines


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Moodle Mate - Your Smart Moodle Notification Assistant"
    )
    parser.add_argument(
        "--gen-config", action="store_true", help="Generate a new configuration file"
    )
    parser.add_argument("--config", default="config.ini", help="Path to config file")
    return parser.parse_args()


@with_retry(max_retries=3, base_delay=5.0, max_delay=30.0)
def fetch_and_process(moodle_handler, notification_processor):
    """Fetch and process notifications with retry logic."""
    if notification := moodle_handler.fetch_newest_notification():
        notification_processor.process(notification)
    return True


def main() -> None:
    """Main entry point of the application."""
    setup_logging()
    args = parse_args()

    if args.gen_config:
        generator = ConfigGenerator()
        if generator.generate_config():
            logging.info("Configuration file generated successfully!")
            sys.exit(0)
        else:
            logging.error("Failed to generate configuration file.")
            sys.exit(1)

    animate_logo(logo_lines)
    logging.info("Starting Moodle Mate...")

    try:
        # Initialize all services
        initialize_services()

        # Get required services from locator
        locator = ServiceLocator()
        config = locator.get("config", Config)
        notification_processor = locator.get(
            "notification_processor", NotificationProcessor
        )
        moodle_handler = locator.get("moodle_handler", MoodleNotificationHandler)

        consecutive_errors = 0
        # Main loop
        while True:
            try:
                success = fetch_and_process(moodle_handler, notification_processor)
                if success:
                    consecutive_errors = 0  # Reset error counter on success

                # Adaptive sleep based on error state
                sleep_time = config.notification.fetch_interval
                if consecutive_errors > 0:
                    # Increase sleep time when experiencing errors
                    sleep_time = min(sleep_time * (2**consecutive_errors), 300)
                time.sleep(sleep_time)

            except Exception as e:
                consecutive_errors += 1
                logging.error(
                    f"Error during execution (attempt {consecutive_errors}): {str(e)}"
                )

                if consecutive_errors >= config.notification.max_retries:
                    logging.critical(
                        "Too many consecutive errors. Restarting main loop..."
                    )
                    consecutive_errors = 0  # Reset counter and continue

                # Exponential backoff sleep on error
                error_sleep = min(30 * (2 ** (consecutive_errors - 1)), 300)
                logging.info(f"Waiting {error_sleep} seconds before retry...")
                time.sleep(error_sleep)

    except KeyboardInterrupt:
        logging.info("Shutting down gracefully...")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()
