from flask import Flask, Blueprint, render_template, request, jsonify, abort
from ai_class import ai_class, AVAILABLE_MODELS, MODEL
# import pdf_reader
from app_logging import setup_logger
from app_logging import reopen_file_handlers
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ------------------------- LOCAL OR PRODUCTION LOCATION ------------------------------ #
# Uncomment for Local development Constant
# LOCATION = ""
# Uncomment for production Waitress server
LOCATION = "/nornnet"

# ------------------------------ LOGGER SETUP ----------------------------------------- #
# Set up logging (file only, no console output by default)
console_output = bool(os.getenv('HTTP_PLATFORM_PORT'))
logger = setup_logger('main_app', 'main_app.log',
                      console_output=console_output)
logger.info("=== main_app.py module loaded ===")
logger.info(f"Python executable: {os.sys.executable}")
logger.info(f"Current working directory: {os.getcwd()}")

# Initialize the AI class instance at module level so all routes can use it
robot = ai_class()

# ------------------------------ RUN LOCALLY OR ON SERVER ------------------------------ #
# Create a Blueprint with /nornnet as the URL prefix
# To run locally: Uncomment the first one, Comment the second one
# nornnet_bp = Blueprint('nornnet', __name__, url_prefix='/', template_folder='templates')
nornnet_bp = Blueprint('nornnet', __name__,
                       url_prefix=LOCATION, template_folder='templates')


@nornnet_bp.route("/", methods=["GET", "POST"])
def hello():
    # Get chat logs
    # Get post is for the user input and ai response
    # set up the input variables for the user and ai
    user_input = ""
    ai_response = ""
    # Reading the pdf each time is inefficient, takes way too much time
    # aiprompt = pdf_reader.read_pdf("student-handbook-25-26.pdf")

    # robot.set_ai_prompt(aiprompt)

    if request.method == "POST":
        try:
            user_input = request.form["user_input"]
            logger.info(f"User question: {user_input}")
            robot.set_user_question(user_input)
            ai_response = robot.get_ai_response()
            logger.info(f"AI response generated successfully")
        except Exception as e:
            logger.error(f"Error processing AI request: {e}")
            ai_response = "Error: Could not connect to NornNet server."

    return render_template("index.html", user_input=user_input, ai_response=ai_response)

# ---------------------------------------------------------------
# NEW Route: /nornnet/models — get available Ollama models
# ---------------------------------------------------------------


@nornnet_bp.route("/models", methods=["GET"])
def get_models():
    """Return list of available Ollama models and the default model."""
    try:
        default_model = os.getenv('DEFAULT_MODEL') or MODEL
        logger.info(
            f"Models endpoint called. Available models: {len(AVAILABLE_MODELS)}; default={default_model}")
        return jsonify({"models": AVAILABLE_MODELS, "default": default_model}), 200
    except Exception as e:
        logger.error(f"Models endpoint error: {e}")
        return jsonify({"models": [], "default": MODEL}), 500


# Internal log test endpoint — call this to force the app to write a test log entry.
# Accessible at /nornnet/__log_test. Intended for debugging only.
@nornnet_bp.route('/__log_test', methods=['GET'])
def __log_test():
    try:
        logger.info('INTERNAL LOG TEST: info entry')
        logger.debug('INTERNAL LOG TEST: debug entry')
        return jsonify({'status': 'ok', 'message': 'log entries written'}), 200
    except Exception as e:
        # If logging itself fails, return the exception so we can diagnose
        return jsonify({'status': 'error', 'error': str(e)}), 500


def validate_turnstile(token: str, secret: str, remoteip: str = None) -> dict:
    """Validate a Cloudflare Turnstile token using the siteverify API.

    Returns the JSON response from Cloudflare (dict).
    """
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    try:
        payload = {"secret": secret, "response": token}
        if remoteip:
            payload["remoteip"] = remoteip
        resp = requests.post(url, data=payload, timeout=5)
        return resp.json()
    except Exception as e:
        logger.error(f"Turnstile validation error: {e}")
        return {"success": False, "error": str(e)}


# ---------------------------------------------------------------
# NEW Route: /nornnet/chat — asynchronous API endpoint for JS fetch()
# ---------------------------------------------------------------
@nornnet_bp.route("/chat", methods=["POST"])
def chat():
    """Handle AJAX chat requests from the frontend and return AI response as JSON."""
    try:
        user_message = request.json.get("message", "").strip()
        selected_model = request.json.get(
            "model", None)  # Get model from request
        # Cloudflare Turnstile token sent from frontend (AJAX)
        turnstile_token = request.json.get('cf-turnstile-response', None)
        # Validate Turnstile if secret configured
        turnstile_secret = os.getenv('TURNSTILE_SECRET')
        if turnstile_secret:
            if not turnstile_token:
                logger.warning('Missing Turnstile token in chat request')
                return jsonify({'reply': 'Verification missing. Please complete the bot check.'}), 400
            remoteip = request.headers.get(
                'CF-Connecting-IP') or request.headers.get('X-Forwarded-For') or request.remote_addr
            valid = validate_turnstile(
                turnstile_token, turnstile_secret, remoteip)
            if not valid.get('success', False):
                logger.warning(f"Turnstile validation failed: {valid}")
                return jsonify({'reply': 'Verification failed. Please try again.'}), 400
        logger.info(f"Received chat message: {user_message}")
        if selected_model:
            logger.info(f"Using model: {selected_model}")

        if not user_message:
            logger.warning("Empty chat message received.")
            return jsonify({"reply": "Please enter a message."}), 400

        # Create AI instance with selected model (or default if None)
        """
            Joe Scott, 11/28/2025
            I commented the ai_class(model=selected_model) bit because
            it was overwritting the chat_logs in the ai class by recreating
            the class object.

            Program works fine without this bit, but I'm unsure what all it
            impacts.
        """
        # robot = ai_class(model=selected_model)
        robot.set_user_question(user_message)
        ai_reply = robot.get_ai_response()

        logger.info("AI reply generated successfully.")
        return jsonify({"reply": ai_reply}), 200

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({"reply": "Error: Could not connect to NornNet server."}), 500


@nornnet_bp.route('/docs')
def docs():
    return render_template('docs.html')


@nornnet_bp.route('/__log_status', methods=['GET'])
def __log_status():
    """Return status of logger handlers (debug endpoint)."""
    try:
        handlers = []
        for h in logger.handlers:
            info = {"type": type(h).__name__}
            if hasattr(h, 'baseFilename'):
                info['baseFilename'] = getattr(h, 'baseFilename')
            if hasattr(h, 'stream'):
                info['stream_open'] = bool(getattr(h, 'stream'))
            handlers.append(info)
        return jsonify({'ok': True, 'handlers': handlers}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@nornnet_bp.route('/__log_reopen', methods=['POST'])
def __log_reopen():
    """Attempt to close and reopen file handlers for the running logger."""
    try:
        results = reopen_file_handlers(logger)
        logger.info("__log_reopen executed")
        return jsonify({'ok': True, 'results': results}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


# Create the Flask app and serve static files under the /cs prefix so
# requests like /cs/static/css/styles.css are handled by Flask.
# This ensures the stylesheet link generated by url_for('static', ...) is
# reachable when the app's routes are under the /nornnet blueprint prefix.
app = Flask(__name__, static_folder='static',
            static_url_path=f'{LOCATION}/static')

# Register the blueprint
app.register_blueprint(nornnet_bp)
logger.info("Blueprint 'nornnet' registered successfully")


@app.context_processor
def inject_globals():
    # Provide the current year to templates for footer
    from datetime import datetime
    # Provide Turnstile site key (optional) so templates can render the widget
    turnstile_site_key = os.getenv('TURNSTILE_SITE_KEY', '')
    turnstile_enabled = bool(os.getenv('TURNSTILE_SECRET')
                             ) and bool(turnstile_site_key)
    return dict(
        current_year=datetime.utcnow().year,
        turnstile_site_key=turnstile_site_key,
        turnstile_enabled=turnstile_enabled
    )


@app.before_request
def log_request():
    """Log each incoming request."""
    logger.info(
        f"Request: {request.method} {request.path} from {request.remote_addr}")


@app.after_request
def log_response(response):
    """Log each response."""
    logger.info(
        f"Response: {request.method} {request.path} - Status {response.status_code}")
    return response


@app.errorhandler(404)
def not_found_error(error):
    """Log 404 errors."""
    logger.warning(f"404 Error: {request.path} from {request.remote_addr}")
    return "Page not found", 404


@app.errorhandler(500)
def internal_error(error):
    """Log 500 errors."""
    logger.error(
        f"500 Error: {request.path} from {request.remote_addr} - {error}")
    return "Internal server error", 500


if __name__ == "__main__":
    logger.info("Starting Flask development server")
    app.run(debug=True)
