"""Module responsible for configuring and providing central logging mechanisms."""

import logging
from pathlib import Path
from typing import Final, Optional
from utils.paths import data_path

# Logging Configuration Constants
LOG_FILE_PATH: Final[Path] = data_path("habit_tracker.log")
LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.INFO) -> None:
    """Configures the root logger handlers and message formatting.

    Creates the required target directories if they do not exist.
    This function must be called once during application startup.

    Args:
        level: The minimum logging severity level (e.g., logging.INFO, logging.DEBUG).
    """
    # Ensure the parent directory for log files exists safely
    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    root_logger: logging.Logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid adding duplicate handlers if setup is called multiple times
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # File Handler for persisting log records
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Console Handler for real-time stdout debugging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Retrieves a named logger instance for modular tracing.

    Args:
        name: The module name invoking the logger (typically __name__).

    Returns:
        A configured logging.Logger instance.
    """
    return logging.getLogger(name)