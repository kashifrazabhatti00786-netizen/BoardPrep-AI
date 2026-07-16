import pytest
import json
from unittest.mock import MagicMock
from backend.app import create_app
from backend.validators.validators import InputValidator

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    """Test standard health checker API route."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "online"

def test_validation_logic():
    """Verify clean string validation boundaries."""
    # Invalid payloads
    err_1 = InputValidator.validate_answer_payload(None)
    assert "Empty" in err_1

    err_2 = InputValidator.validate_answer_payload({
        "subject": "Physics",
        "question": "Short",
        "answer": "Too small",
        "board": "Lahore",
        "grade": "Matric-10"
    })
    assert "too short" in err_2 or "Too short" in err_2 or "short" in err_2

    # Valid payload
    err_3 = InputValidator.validate_answer_payload({
        "subject": "Chemistry",
        "question": "Write the periodic table properties of Alkali metals.",
        "answer": "Alkali metals occupy group 1 of the periodic table, showing highly reactive characteristics...",
        "board": "Faisalabad",
        "grade": "FSc-1"
    })
    assert err_3 is None
