"""
Filename: waitress_app.py
Description: This script sets up and runs a Waitress WSGI server
to serve a Flask web application.
"""

from main_app import app
import os
from sys import path
from app_logging import setup_logger

# Add current directory to path to ensure imports work
path.insert(0, os.path.dirname(os.path.abspath(__file__)))

THREADS = 64

# Set up logging (file only; no console output)
logger = setup_logger('waitress_app', 'waitress_app.log', console_output=False)
logger.info(f"Current working directory: {os.getcwd()}")
logger.info("Flask app imported successfully")


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
        logger.info(f"Calling serve with threads={THREADS}, connection_limit=1000")
        
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
    logger.info("Running as main script")
    main()
else:
    logger.info("Module imported by IIS")
