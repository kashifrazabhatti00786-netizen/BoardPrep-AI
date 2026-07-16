class InputValidator:
    """Utility class to validate client inputs and avoid injection or dirty strings."""

    @staticmethod
    def validate_answer_payload(data):
        """Validates incoming answer check parameters. Returns error description or None."""
        if not data:
            return "Empty payload details."

        required = ["subject", "question", "answer", "board", "grade"]
        for key in required:
            if key not in data or not str(data[key]).strip():
                return f"Missing value for field: {key}"

        # Check string length criteria
        if len(data["answer"]) < 10:
            return "Answer is too short to evaluate properly."
        if len(data["question"]) < 5:
            return "Question is too short."

        return None

    @staticmethod
    def validate_topic_payload(data):
        """Validates incoming topic payload parameters. Returns error description or None."""
        if not data:
            return "Empty payload details."

        required = ["subject", "topic", "board", "grade"]
        for key in required:
            if key not in data or not str(data[key]).strip():
                return f"Missing value for field: {key}"

        return None
