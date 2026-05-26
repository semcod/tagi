"""Logging module for tagi."""

import logging
import sys
from pathlib import Path
from typing import Optional


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
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG if verbose else level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "tagi") -> logging.Logger:
    """Get existing logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
