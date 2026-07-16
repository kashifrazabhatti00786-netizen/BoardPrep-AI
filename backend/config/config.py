import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

class Config:
    """Base Configuration class containing shared environment settings."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "prod-super-secret-key-boardprep")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

    # Firebase configuration
    FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
    FIREBASE_PRIVATE_KEY = os.environ.get("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n") if os.environ.get("FIREBASE_PRIVATE_KEY") else ""
    FIREBASE_CLIENT_EMAIL = os.environ.get("FIREBASE_CLIENT_EMAIL", "")

    # Firestore configurations
    FIRESTORE_DATABASE_ID = os.environ.get("FIRESTORE_DATABASE_ID", "(default)")

    @classmethod
    def validate(cls):
        """Validates critical config values. Returns a dict of missing keys."""
        missing = []
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not cls.FIREBASE_PROJECT_ID:
            missing.append("FIREBASE_PROJECT_ID")
        if not cls.FIREBASE_PRIVATE_KEY:
            missing.append("FIREBASE_PRIVATE_KEY")
        if not cls.FIREBASE_CLIENT_EMAIL:
            missing.append("FIREBASE_CLIENT_EMAIL")
        return missing
