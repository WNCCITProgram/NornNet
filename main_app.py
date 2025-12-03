from flask import Flask, Blueprint, render_template, request, jsonify, abort
from ai_class import ai_class, AVAILABLE_MODELS, MODEL
# import pdf_reader
import os
import requests
from dotenv import load_dotenv
from app_logging import configure_loguru
from loguru import logger

# Load environment variables from .env file
load_dotenv()

# ------------------------- LOCAL OR PRODUCTION LOCATION ------------------------------ #
# Uncomment for Local development Constant
# LOCATION = ""
# Uncomment for production Waitress server
LOCATION = "/nornnet"

# ------------------------------ LOGGER SETUP ----------------------------------------- #
# logging removed
console_output = bool(os.getenv('HTTP_PLATFORM_PORT'))
configure_loguru(app_name="main_app", filename="main_app.log", console_output=console_output)
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
        return jsonify({"models": AVAILABLE_MODELS, "default": default_model}), 200
    except Exception:
        return jsonify({"models": [], "default": MODEL}), 500


# Debug logging endpoints removed


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
        # logging removed
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
                return jsonify({'reply': 'Verification missing. Please complete the bot check.'}), 400
            remoteip = request.headers.get(
                'CF-Connecting-IP') or request.headers.get('X-Forwarded-For') or request.remote_addr
            valid = validate_turnstile(
                turnstile_token, turnstile_secret, remoteip)
            if not valid.get('success', False):
                return jsonify({'reply': 'Verification failed. Please try again.'}), 400
        # logging removed

        if not user_message:
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

        return jsonify({"reply": ai_reply}), 200

    except Exception:
        return jsonify({"reply": "Error: Could not connect to NornNet server."}), 500


@nornnet_bp.route('/docs')
def docs():
    return render_template('docs.html')


# Debug logging endpoints removed


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

if __name__ == "__main__":
    app.run(debug=True)

# Request/response logging similar to previous setup
@app.before_request
def _log_request_info():
    try:
        logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
    except Exception:
        pass


@app.after_request
def _log_response_info(response):
    try:
        logger.info(f"Response: {request.method} {request.path} - Status {response.status_code}")
    except Exception:
        pass
    return response


@app.errorhandler(404)
def _not_found_error(error):
    try:
        logger.warning(f"404 Error: {request.path} from {request.remote_addr}")
    except Exception:
        pass
    return "Page not found", 404


@app.errorhandler(500)
def _internal_error(error):
    try:
        logger.error(f"500 Error: {request.path} from {request.remote_addr} - {error}")
    except Exception:
        pass
    return "Internal server error", 500
