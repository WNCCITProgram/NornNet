"""
Filename: app_logging.py
Description: Centralized logging configuration using Loguru for NornNet.
Sets up file-based logging with daily rotation for main_app.
"""

import os
from loguru import logger


def configure_loguru(app_name: str = "main_app", filename: str = "main_app.log", console_output: bool = True):
	"""Configure Loguru to write daily-rotated logs under /logs.

	- rotation: at midnight
	- retention: 7 days
	- enqueue: True for process-safe logging under IIS/Waitress
	- format: time level message
	"""
	script_dir = os.path.dirname(os.path.abspath(__file__))
	log_dir = os.path.join(script_dir, "logs")
	os.makedirs(log_dir, exist_ok=True)

	log_path = os.path.join(log_dir, filename)

	# Remove default sinks to avoid duplicates on recycle
	logger.remove()

	# File sink: daily rotation at midnight, keep 7 days
	logger.add(
		log_path,
		rotation="00:00",
		retention="7 days",
		encoding="utf-8",
		enqueue=True,
		backtrace=False,
		diagnose=False,
		format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}"
	)

	# Optional console sink for local debugging or IIS stdout
	if console_output:
		logger.add(
			lambda msg: print(msg, end=""),
			level="INFO",
			format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}"
		)

	logger.info(f"Logger configured for {app_name}. File: {log_path}")
	return logger
