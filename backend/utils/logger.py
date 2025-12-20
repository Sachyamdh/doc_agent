import logging
import sys
import os


class CustomFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format_str = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(
            log_fmt, datefmt="%Y-%m-%d %H:%M:%S"
        )
        return formatter.format(record)


def setup_logger(name: str, level: str = None) -> logging.Logger:
    """
    Create and configure a console-only logger

    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()

    log_level = getattr(logging, level, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(CustomFormatter())

    logger.addHandler(console_handler)

    return logger


def log_exception(logger: logging.Logger, exception: Exception, context: str = ""):
    """Log an exception with full traceback"""
    if context:
        logger.error(f"{context}: {exception}", exc_info=True)
    else:
        logger.error(f"Exception occurred: {exception}", exc_info=True)


def log_function_call(logger: logging.Logger):
    """
    Decorator to log function entry and exit
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(
                f"Entering {func.__name__} with args={args}, kwargs={kwargs}"
            )
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Exiting {func.__name__} successfully")
                return result
            except Exception as e:
                logger.error(
                    f"Error in {func.__name__}: {e}", exc_info=True
                )
                raise
        return wrapper
    return decorator
