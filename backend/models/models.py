class UserProfile:
    """Domain model representing a student user account."""
    def __init__(self, uid, email, display_name=None, board=None, grade=None):
        self.uid = uid
        self.email = email
        self.display_name = display_name or ""
        self.board = board or "Lahore"
        self.grade = grade or "Matric-10"

    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "displayName": self.display_name,
            "board": self.board,
            "grade": self.grade
        }

class AnswerEvaluation:
    """Domain model representing a evaluated Punjab board response."""
    def __init__(self, answer_id, student_id, subject, question, answer, score, max_score, rubric_match, presentation, diagrams, corrections, timestamp=None):
        self.answer_id = answer_id
        self.student_id = student_id
        self.subject = subject
        self.question = question
        self.answer = answer
        self.score = score
        self.max_score = max_score
        self.rubric_match = rubric_match
        self.presentation = presentation
        self.diagrams = diagrams
        self.corrections = corrections
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "answerId": self.answer_id,
            "studentId": self.student_id,
            "subject": self.subject,
            "question": self.question,
            "answer": self.answer,
            "score": self.score,
            "max_score": self.max_score,
            "rubric_match": self.rubric_match,
            "presentation": self.presentation,
            "diagrams": self.diagrams,
            "corrections": self.corrections,
            "timestamp": self.timestamp
        }
