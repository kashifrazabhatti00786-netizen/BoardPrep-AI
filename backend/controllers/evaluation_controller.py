import os
import uuid
from datetime import datetime
from flask import jsonify, request, g
from backend.validators.validators import InputValidator
from backend.services.ai_service import GeminiService
from backend.repositories.repository import FirestoreRepository

# Instantiate Service and Repository safely
ai_service = GeminiService()
try:
    db_repo = FirestoreRepository()
except Exception as e:
    # If Firebase credentials aren't loaded or initialized
    db_repo = None

class EvaluationController:
    """Handles incoming student answer check and topic parsing endpoints."""

    @staticmethod
    def check_answer():
        data = request.get_json()
        validation_error = InputValidator.validate_answer_payload(data)
        if validation_error:
            return jsonify({"message": validation_error}), 400

        try:
            result = ai_service.check_answer(
                subject=data["subject"],
                question=data["question"],
                answer=data["answer"],
                board=data["board"],
                grade=data["grade"]
            )

            # Persist answer evaluation result to Firestore Repository if user authenticated & DB exists
            if db_repo and hasattr(g, 'user') and g.user:
                student_id = g.user.get("uid")
                answer_id = str(uuid.uuid4())
                eval_record = {
                    "answerId": answer_id,
                    "studentId": student_id,
                    "subject": data["subject"],
                    "question": data["question"],
                    "answer": data["answer"],
                    "score": result.get("score", 3.0),
                    "max_score": result.get("max_score", 4.0),
                    "rubric_match": result.get("rubric_match", 75),
                    "presentation": result.get("presentation", ""),
                    "diagrams": result.get("diagrams", ""),
                    "corrections": result.get("corrections", ""),
                    "timestamp": datetime.utcnow().isoformat()
                }
                try:
                    db_repo.save_answer_evaluation(answer_id, eval_record)
                except Exception as db_err:
                    # Non-blocking log
                    pass

            return jsonify(result), 200
        except Exception as e:
            return jsonify({"message": "Failed during AI checker cycle.", "error": str(e)}), 500

    @staticmethod
    def analyze_topic():
        data = request.get_json()
        validation_error = InputValidator.validate_topic_payload(data)
        if validation_error:
            return jsonify({"message": validation_error}), 400

        try:
            result = ai_service.analyze_topic(
                subject=data["subject"],
                topic=data["topic"],
                board=data["board"],
                grade=data["grade"]
            )
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"message": "Failed during topic analysis cycle.", "error": str(e)}), 500
