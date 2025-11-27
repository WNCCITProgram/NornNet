"""
Filename: waitress_app.py
Description: This script sets up and runs a Waitress WSGI server
to serve a Flask web application.
"""

import os
import sys
from sys import path

# Add current directory to path to ensure imports work
path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging BEFORE importing main_app
from app_logging import setup_logger
is_iis = bool(os.getenv('HTTP_PLATFORM_PORT'))
logger = setup_logger('waitress_app', 'waitress_app.log', console_output=is_iis)
logger.info(f"=== Waitress startup at {os.getpid()} ===")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python version: {sys.version}")

# Flush immediately to ensure log writes
for handler in logger.handlers:
    handler.flush()

# Now import the Flask app
try:
    from main_app import app
    logger.info("Flask app imported successfully")
    for handler in logger.handlers:
        handler.flush()
except Exception as e:
    logger.error(f"Failed to import main_app: {e}")
    for handler in logger.handlers:
        handler.flush()
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
    
    # Force flush logs
    for handler in logger.handlers:
        handler.flush()

    try:
        from waitress import serve
        logger.info(f"About to call serve() with app={app}, host={host}, port={port}")
        logger.info(f"Calling serve with threads={THREADS}, connection_limit=1000")
        
        # Force flush before blocking call
        for handler in logger.handlers:
            handler.flush()
        
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
    for handler in logger.handlers:
        handler.flush()
    main()
else:
    logger.info("Module imported by IIS")
    for handler in logger.handlers:
        handler.flush()
