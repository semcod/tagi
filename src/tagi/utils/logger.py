"""Logging module for tagi."""

import logging
import sys
from pathlib import Path
from typing import Optional


def _build_formatter() -> logging.Formatter:
    """Build the formatter shared by all tagi handlers."""
    return logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def _build_console_handler(level: int, verbose: bool) -> logging.Handler:
    """Build the stderr console handler."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG if verbose else level)
    handler.setFormatter(_build_formatter())
    return handler


def _add_file_handler(logger: logging.Logger, log_file: str) -> None:
    """Attach a DEBUG-level file handler, creating parent directories."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(_build_formatter())
    logger.addHandler(file_handler)


def setup_logger(
    name: str = "tagi",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    verbose: bool = False
) -> logging.Logger:
    """Setup and configure logger for tagi.

    Args:
        name: Logger name
        level: Logging level (default: INFO)
        log_file: Optional path to log file
        verbose: Enable DEBUG level logging

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Remove existing handlers
    logger.handlers.clear()

    # Set level
    logger.setLevel(logging.DEBUG if verbose else level)

    # Console handler
    logger.addHandler(_build_console_handler(level, verbose))

    # File handler (optional)
    if log_file:
        _add_file_handler(logger, log_file)

    return logger


def get_logger(name: str = "tagi") -> logging.Logger:
    """Get existing logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
