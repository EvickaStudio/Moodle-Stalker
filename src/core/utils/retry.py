import logging
import time
from functools import wraps
from typing import Callable, Optional, TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)


def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,),
    on_failure: Optional[Callable] = None,
) -> Callable:
    """
    Decorator that implements retry logic with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exceptions: Tuple of exceptions to catch and retry
        on_failure: Optional callback function to execute when all retries fail
    """

    def decorator(func: Callable[..., T]) -> Callable[..., Optional[T]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[T]:
            retries = 0
            delay = base_delay

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(
                            f"Maximum retries ({max_retries}) exceeded for {func.__name__}: {str(e)}"
                        )
                        if on_failure:
                            return on_failure()
                        return None

                    logger.warning(
                        f"Attempt {retries}/{max_retries} failed for {func.__name__}: {str(e)}"
                        f"\nRetrying in {delay} seconds..."
                    )
                    time.sleep(delay)
                    delay = min(delay * 2, max_delay)  # Exponential backoff

        return wrapper

    return decorator
