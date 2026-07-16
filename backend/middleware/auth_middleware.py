from functools import wraps
from flask import request, g, jsonify
import firebase_admin
from firebase_admin import auth

def require_firebase_auth(f):
    """Secure middleware verifying incoming requests carry verified JWT tokens from Firebase client."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing authorization credentials."}), 401

        token = auth_header.split("Bearer ")[1].strip()
        try:
            # Verify the Firebase ID Token
            decoded_token = auth.verify_id_token(token)
            g.user = decoded_token
        except Exception as e:
            # We return 401 for unauthorized or expired credentials
            return jsonify({"message": "Invalid or expired session token.", "error": str(e)}), 401

        return f(*args, **kwargs)
    return decorated_function
