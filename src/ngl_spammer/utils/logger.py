"""Logging utilities for NGL Link Spammer."""

import logging
import sys
from typing import Optional

from .config import config


def setup_logger(
    name: str = "ngl_spammer",
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Set up and configure logger.
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom log format string
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Set level
    log_level = level or config.log_level
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logger.level)
    
    # Create formatter
    formatter = logging.Formatter(format_string or config.log_format)
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    return logger


# Global logger instance
logger = setup_logger()
