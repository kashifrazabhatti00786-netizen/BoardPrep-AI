from flask import Blueprint
from backend.controllers.evaluation_controller import EvaluationController
from backend.middleware.auth_middleware import require_firebase_auth

api_blueprint = Blueprint("api_blueprint", __name__)

# Register exact endpoints
api_blueprint.route("/check-answer", methods=["POST"])(require_firebase_auth(EvaluationController.check_answer))
api_blueprint.route("/analyze-topic", methods=["POST"])(require_firebase_auth(EvaluationController.analyze_topic))
