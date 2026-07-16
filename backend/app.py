import os
from flask import Flask, jsonify
from flask_cors import CORS
from backend.config.config import Config
from backend.routes.api import api_blueprint

def create_app():
    """Application factory for BoardPrep AI Flask backend."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable secure Cross-Origin Resource Sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register routes blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    @app.route("/health", methods=["GET"])
    def health_check():
        """SaaS healthcheck endpoint."""
        missing_vars = Config.validate()
        return jsonify({
            "status": "online",
            "firebase_configured": not bool("FIREBASE_PROJECT_ID" in missing_vars),
            "gemini_configured": not bool("GEMINI_API_KEY" in missing_vars),
            "missing_keys": missing_vars
        }), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Target endpoint resource not found."}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"message": "An internal server event error occurred."}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
