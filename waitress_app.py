"""
Filename: waitress_app.py
Description: This script sets up and runs a Waitress WSGI server
to serve a Flask web application.
"""

import os
import sys
from sys import path
from app_logging import configure_loguru
from loguru import logger

# Add current directory to path to ensure imports work
path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging for waitress_app with daily rotation under logs/
console_output = bool(os.getenv('HTTP_PLATFORM_PORT'))
configure_loguru(app_name="waitress_app", filename="waitress_app.log", console_output=console_output)
logger.info("=== Waitress startup ===")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python version: {sys.version}")

# Now import the Flask app
try:
    from main_app import app
    logger.info("Flask app imported successfully")
except Exception as e:
    logger.error(f"Failed to import main_app: {e}")
    raise

THREADS = 64


def main():
    # Determine port from environment (HTTP_PLATFORM_PORT set by IIS httpPlatform handler,
    # or PORT common in other hosting environments). Fall back to 8080 if unset or invalid.
    port_env = os.environ.get("HTTP_PLATFORM_PORT") or os.environ.get("PORT")
    try:
        port = int(port_env) if port_env else 8080
    except Exception:
        port = 8080

    # Bind to all interfaces so the IIS front-end or reverse-proxy can reach the server.
    host = os.environ.get("HOST") or "0.0.0.0"
    logger.info(f"Starting Waitress server on {host}:{port}")
    logger.info(f"HTTP_PLATFORM_PORT raw: {os.environ.get('HTTP_PLATFORM_PORT', 'NOT SET')}")
    logger.info(f"PORT raw: {os.environ.get('PORT', 'NOT SET')}")
    logger.info(f"Host binding: {host}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Python PID: {os.getpid()}")

    
    try:
        from waitress import serve
        logger.info(f"About to call serve() with app={app}, host={host}, port={port}")
        logger.info("Calling serve with threads=64, connection_limit=1000")
        # Call serve - this blocks until server stops
        serve(
            app,
            host=host,
            port=port,
            threads=THREADS,
            connection_limit=1000,
            channel_timeout=120,
            _start=True  # Ensure server starts immediately
        )
        logger.warning("serve() returned (this shouldn't happen)")
    except Exception as e:
        import traceback
        error_msg = f"Failed to start Waitress: {e}\n{traceback.format_exc()}"
        logger.error(error_msg)
        exit(1)


if __name__ == "__main__":
    main()
