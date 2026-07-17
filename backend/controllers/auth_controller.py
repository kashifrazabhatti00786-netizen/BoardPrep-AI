from flask import request, g, jsonify
from datetime import datetime
from backend.repositories.repository import FirestoreRepository

class AuthController:
    """Controller layer managing user registration, profile initialization, and secure session checking."""

    @staticmethod
    def signup():
        """Registers a newly authenticated Firebase user in Firestore with secure default values."""
        if not g.user:
            return jsonify({"message": "Unauthorized. Missing authentication context."}), 401

        uid = g.user.get("uid")
        email = g.user.get("email")

        try:
            data = request.get_json() or {}
            full_name = data.get("fullName", "").strip()
            whatsapp_number = data.get("whatsappNumber", "").strip()

            if not full_name:
                return jsonify({"message": "Full name is required."}), 400

            if not whatsapp_number:
                return jsonify({"message": "WhatsApp number is required."}), 400

            repo = FirestoreRepository()
            existing_profile = repo.get_user_profile(uid)

            if existing_profile:
                return jsonify({"message": "User profile already initialized.", "profile": existing_profile}), 200

            # Default secure parameters
            profile = {
                "uid": uid,
                "fullName": full_name,
                "email": email,
                "whatsappNumber": whatsapp_number,
                "role": "user",
                "plan": "free",
                "emailVerified": g.user.get("email_verified", False),
                "profileImage": None,
                "createdAt": datetime.utcnow().isoformat(),
                "updatedAt": datetime.utcnow().isoformat(),
                "accountStatus": "active",
                "banned": False,
                "questionChecksUsed": 0,
                "topicAnalysisUsed": 0,
                "supportTickets": 0
            }

            repo.save_user_profile(uid, profile)
            return jsonify({"message": "User profile initialized successfully.", "profile": profile}), 201

        except Exception as e:
            return jsonify({"message": "An internal error occurred during profile initialization.", "error": str(e)}), 500

    @staticmethod
    def check_session():
        """Validates authenticated session tokens and inspects user ban/active status before granting entrance."""
        if not g.user:
            return jsonify({"message": "Unauthorized. Missing authentication context."}), 401

        uid = g.user.get("uid")

        try:
            repo = FirestoreRepository()
            profile = repo.get_user_profile(uid)

            if not profile:
                # If the profile document doesn't exist yet but user is authenticated, we return profile missing
                return jsonify({"message": "User profile is not registered in the database."}), 404

            if profile.get("banned", False) or profile.get("accountStatus") != "active":
                return jsonify({
                    "message": "Access denied. Your account has been suspended or deactivated. Please reach support."
                }), 403

            # Update email verification status if changed in client token
            email_verified_now = g.user.get("email_verified", False)
            if email_verified_now != profile.get("emailVerified"):
                profile["emailVerified"] = email_verified_now
                profile["updatedAt"] = datetime.utcnow().isoformat()
                repo.save_user_profile(uid, {"emailVerified": email_verified_now, "updatedAt": profile["updatedAt"]})

            return jsonify({
                "message": "Session is active and valid.",
                "user": {
                    "uid": profile.get("uid"),
                    "fullName": profile.get("fullName"),
                    "email": profile.get("email"),
                    "role": profile.get("role"),
                    "plan": profile.get("plan")
                }
            }), 200

        except Exception as e:
            return jsonify({"message": "An internal error occurred during session verification.", "error": str(e)}), 500
