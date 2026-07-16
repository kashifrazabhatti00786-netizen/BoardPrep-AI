import firebase_admin
from firebase_admin import credentials, firestore
from backend.config.config import Config

class FirestoreRepository:
    """Clean Repository Layer separating Firestore logic from other routes."""

    def __init__(self):
        # Initialize Firebase Admin safely if it's not already initialized
        if not firebase_admin._apps:
            # We check if local private key env matches or we load mock
            if Config.FIREBASE_PROJECT_ID and Config.FIREBASE_PRIVATE_KEY:
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": Config.FIREBASE_PROJECT_ID,
                    "private_key": Config.FIREBASE_PRIVATE_KEY,
                    "client_email": Config.FIREBASE_CLIENT_EMAIL,
                    "token_uri": "https://oauth2.googleapis.com/token"
                })
                firebase_admin.initialize_app(cred)
            else:
                # Local mock initialization or default environment setup
                firebase_admin.initialize_app()

        self.db = firestore.client()

    def get_user_profile(self, uid):
        """Loads student profile from database."""
        ref = self.db.collection("users").document(uid).get()
        return ref.to_dict() if ref.exists else None

    def save_user_profile(self, uid, profile_dict):
        """Saves or merges student profile to database."""
        self.db.collection("users").document(uid).set(profile_dict, merge=True)

    def save_answer_evaluation(self, answer_id, evaluation_dict):
        """Persists evaluated answer sheet to database."""
        self.db.collection("answers").document(answer_id).set(evaluation_dict)

    def get_answer_history(self, student_id):
        """Loads history entries for a specific student."""
        docs = self.db.collection("answers").where("studentId", "==", student_id).stream()
        return [doc.to_dict() for doc in docs]
