"""Logging setup for the edge mental health agent."""

import logging
import os
from pathlib import Path
from typing import Optional

from .config import load_config


def setup_logging(level: Optional[str] = None, log_file: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        
    Returns:
        Configured logger instance
    """
    try:
        config = load_config()
        logging_config = config.get("logging", {})
    except (FileNotFoundError, KeyError):
        logging_config = {}
    
    # Use provided arguments or fall back to config or defaults
    level = level or logging_config.get("level", "INFO")
    log_format = logging_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log_file = log_file or logging_config.get("file")
    
    # Create logs directory if needed
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=handlers,
        force=True  # Override any existing configuration
    )
    
    logger = logging.getLogger("edge_mental_health_agent")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name.
    
    Args:
        name: Name for the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"edge_mental_health_agent.{name}")
