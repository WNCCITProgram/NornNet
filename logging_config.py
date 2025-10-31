"""
Filename: logging_config.py
Description: Centralized logging configuration for the NornNet application.
Sets up file-based logging with daily rotation for both main_app and waitress_app.
"""

import logging
import logging.handlers
import os
import re


def setup_logger(logger_name, log_filename, console_output=False):
    """
    Set up a logger with file rotation and optional console output.
    
    Args:
        logger_name (str): Name of the logger (e.g., 'main_app', 'waitress_app')
        log_filename (str): Base name of the log file (e.g., 'main_app.log')
        console_output (bool): Whether to also output logs to console (default: False)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get the absolute path to this script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "logs")
    log_file = os.path.join(log_dir, log_filename)
    
    # Ensure logs directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Get or create the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers from this logger
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Use TimedRotatingFileHandler for daily rotation
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    
    # Set date suffix format for rotated files: logfile.log.2025-10-30
    file_handler.suffix = "%Y-%m-%d"
    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    
    # Set formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    # Log initialization
    logger.info(f"=== Logger '{logger_name}' initialized ===")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Console output: {console_output}")
    
    return logger
