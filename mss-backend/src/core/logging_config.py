"""
Logging Configuration Module

Sets up structured logging with appropriate formatters and handlers
for different environments.
"""

import logging
import logging.config
from src.core.config import settings
from datetime import datetime


def setup_logging(name: str) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    
    # Log format
    if settings.DEBUG:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )
    else:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional, for production)
    if settings.ENVIRONMENT == "production":
        log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
        try:
            file_handler = logging.FileHandler(log_filename)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not create file handler: {e}")
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


# Configure root logger
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
