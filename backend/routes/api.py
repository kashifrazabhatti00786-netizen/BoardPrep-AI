from flask import Blueprint
from backend.controllers.evaluation_controller import EvaluationController
from backend.controllers.auth_controller import AuthController
from backend.middleware.auth_middleware import require_firebase_auth

api_blueprint = Blueprint("api_blueprint", __name__)

# Evaluation Endpoints
api_blueprint.route("/check-answer", methods=["POST"])(require_firebase_auth(EvaluationController.check_answer))
api_blueprint.route("/analyze-topic", methods=["POST"])(require_firebase_auth(EvaluationController.analyze_topic))

# Authentication & Session Endpoints
api_blueprint.route("/auth/signup", methods=["POST"])(require_firebase_auth(AuthController.signup))
api_blueprint.route("/auth/session", methods=["POST"])(require_firebase_auth(AuthController.check_session))
