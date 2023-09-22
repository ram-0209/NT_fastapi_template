"""Logger Decorator"""
import functools

from loguru import logger


def logger_wraps(*, entry=True, exit=True, level="DEBUG"):
    """Logger Wraps

    Args:
        entry (bool, optional):  Defaults to True.
        exit (bool, optional): Defaults to True.
        level (str, optional):  Defaults to "DEBUG".
    """

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}'", name)
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' ", name)
            return result

        return wrapped

    return wrapper
