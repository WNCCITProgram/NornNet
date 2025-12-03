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
import socket
import traceback

# Add current directory to path to ensure imports work
path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging for waitress_app with daily rotation under logs/
console_output = bool(os.getenv('HTTP_PLATFORM_PORT'))
configure_loguru(app_name="waitress_app", filename="waitress_app.log", console_output=console_output)
logger.info("=== Waitress startup ===")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Executable: {sys.executable}")
logger.info(f"Process PID: {os.getpid()}")
logger.info(f"Platform: {sys.platform}")
logger.info(f"Hostname: {socket.gethostname()}")

# Now import the Flask app
try:
    from main_app import app
    logger.info("Flask app imported successfully")
except Exception as e:
    logger.error(f"Failed to import main_app: {e}")
    raise

THREADS = 64


def main():
    # --- Environment diagnostics ---
    env_keys = [
        "HTTP_PLATFORM_PORT", "PORT", "HOST",
        "WEBSITE_SITE_NAME", "COMPUTERNAME", "PROCESSOR_IDENTIFIER",
        "APP_POOL_ID", "USERNAME"
    ]
    for k in env_keys:
        v = os.environ.get(k, "NOT SET")
        logger.info(f"ENV {k} = {v}")

    # Ensure logs directory exists and is writable
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    try:
        os.makedirs(logs_dir, exist_ok=True)
        test_path = os.path.join(logs_dir, ".write_test")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(test_path)
        logger.info(f"Logs directory OK: {logs_dir}")
    except Exception as e:
        logger.warning(f"Logs directory check failed: {e}")

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

    # Route diagnostics
    try:
        from werkzeug.routing import Rule
        logger.info("=== Flask URL Map ===")
        for rule in app.url_map.iter_rules():
            methods = ",".join(sorted(rule.methods)) if hasattr(rule, "methods") else ""
            logger.info(f"Rule: {rule.rule} -> endpoint={rule.endpoint} methods=[{methods}]")
    except Exception as e:
        logger.warning(f"Could not enumerate URL map: {e}")

    # Resolve local addresses
    try:
        host_ips = socket.gethostbyname_ex(socket.gethostname())
        logger.info(f"Local IPs: {host_ips[2]}")
    except Exception as e:
        logger.warning(f"Hostname resolution failed: {e}")

    
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
        error_msg = f"Failed to start Waitress: {e}\n{traceback.format_exc()}"
        logger.error(error_msg)
        exit(1)
    except KeyboardInterrupt:
        logger.info("Waitress shutdown requested by KeyboardInterrupt")
    finally:
        logger.info("Waitress main() finished")


if __name__ == "__main__":
    main()
