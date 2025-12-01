"""
Filename: app_logging.py
Description: Centralized logging configuration for the NornNet application.
Sets up file-based logging with daily rotation for both main_app and waitress_app.
"""

import logging
import logging.handlers
import os


class FlushingTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Custom handler that forces immediate flushing after every log entry.
    Critical for IIS/Waitress environments where logs may not appear otherwise.
    """

    def emit(self, record):
        super().emit(record)
        if self.stream:
            self.stream.flush()


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

    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "logs")
    log_file = os.path.join(log_dir, log_filename)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler = None
    handler_type = "FlushingTimedRotatingFileHandler"
    try:
        file_handler = FlushingTimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8", delay=True
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.debug("Attached FlushingTimedRotatingFileHandler successfully.")
    except Exception as e:
        # Fallback to RotatingFileHandler if custom handler fails
        handler_type = "RotatingFileHandler (fallback)"
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=5*1024*1024, backupCount=7, encoding="utf-8", delay=True
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.error(f"Failed to attach FlushingTimedRotatingFileHandler: {e}. Using fallback RotatingFileHandler.")
        except Exception as e2:
            logger.critical(f"Failed to attach any file handler: {e2}")

    if console_output:
        try:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            logger.debug("Console handler attached.")
        except Exception as e:
            logger.error(f"Failed to attach console handler: {e}")

    logger.propagate = False
    logger.info(f"=== Logger '{logger_name}' initialized ({handler_type}) ===")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Console output: {console_output}")
    logger.debug(f"Logger handlers: {[type(h).__name__ for h in logger.handlers]}")
    return logger


def reopen_file_handlers(logger: logging.Logger) -> dict:
    """
    Attempt to close and reopen any file-based handlers attached to the provided logger.

    Returns a dict with results for each handler.
    """
    results = {}
    for i, handler in enumerate(list(logger.handlers)):
        name = type(handler).__name__
        key = f"handler_{i}_{name}"
        results[key] = {"type": name}
        try:
            if hasattr(handler, "baseFilename"):
                filename = getattr(handler, "baseFilename")
                results[key]["baseFilename"] = filename
                try:
                    handler.flush()
                except Exception:
                    pass
                try:
                    handler.close()
                except Exception as e:
                    results[key]["close_error"] = str(e)
                try:
                    logger.removeHandler(handler)
                except Exception:
                    pass

                # Recreate a FlushingTimedRotatingFileHandler if possible
                try:
                    newh = FlushingTimedRotatingFileHandler(filename, when="midnight", interval=1, backupCount=7, encoding="utf-8", delay=True)
                    newh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
                    logger.addHandler(newh)
                    results[key]["reopened"] = True
                except Exception as e:
                    # Fallback to RotatingFileHandler
                    try:
                        newh = logging.handlers.RotatingFileHandler(filename, maxBytes=5*1024*1024, backupCount=7, encoding="utf-8", delay=True)
                        newh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
                        logger.addHandler(newh)
                        results[key]["reopened"] = "rotating_fallback"
                    except Exception as e2:
                        results[key]["reopened"] = False
                        results[key]["reopen_error"] = f"{e}; fallback: {e2}"
            else:
                results[key]["note"] = "not a file handler"
        except Exception as e:
            results[key]["error"] = str(e)
    return results
