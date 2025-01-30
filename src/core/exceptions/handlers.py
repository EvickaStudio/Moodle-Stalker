import logging
import sys
import traceback

logger = logging.getLogger(__name__)


def handle_exceptions(func):
    """
    Decorator to handle exceptions in a standardized way across methods.
    Logs the exception and returns None in case of an error.

    :param func: The function to decorate.
    :return: Wrapped function with exception handling.
    """

    def wrapper(*args, **kwargs):
        """
        Wrapper function to execute the decorated function and handle exceptions.
        Logs exceptions and returns None in case of an error.

        :param args: Arguments passed to the decorated function.
        :param kwargs: Keyword arguments passed to the decorated function.
        :return: The result of the decorated function or None if an exception occurred.
        """
        try:
            result = func(*args, **kwargs)
        except BaseException as e:
            logger.exception(f"Exception occurred in {func.__name__}: {str(e)}")
            _, err, tb = sys.exc_info()
            logger.debug(traceback.format_tb(err.__traceback__)[-1])
            return None
        else:
            return result

    return wrapper
