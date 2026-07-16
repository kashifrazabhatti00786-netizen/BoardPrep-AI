import google.generativeai as genai
import json
from backend.config.config import Config
from backend.prompts.prompts import get_answer_checker_system_prompt, get_topic_analyzer_system_prompt

class GeminiService:
    """Core Service Layer interacting directly with Google's Gemini API."""

    def __init__(self):
        # Configure Gemini safely
        api_key = Config.GEMINI_API_KEY
        if api_key:
            genai.configure(api_key=api_key)
        # Use gemini-1.5-flash which supports response_mime_type and is fast and stable
        self.model_name = "gemini-1.5-flash"

    def check_answer(self, subject, question, answer, board, grade):
        """Analyzes student answer against BISE grading standards using Gemini API."""
        try:
            prompt = (
                f"Subject: {subject}\n"
                f"Question: {question}\n"
                f"Student's Answer: {answer}\n"
                f"Board: {board}\n"
                f"Grade Level: {grade}"
            )

            system_prompt = get_answer_checker_system_prompt(subject, board, grade)

            # Using generative model model instance
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={"response_mime_type": "application/json"}
            )

            # Combine system prompt guidelines
            response = model.generate_content(f"{system_prompt}\n\n{prompt}")

            # Safely parse returned JSON payload
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif clean_text.startswith("```"):
                clean_text = clean_text.split("```")[1].split("```")[0].strip()

            return json.loads(clean_text)

        except Exception as e:
            # Safe Fallback to standard structured mock answer if offline or API Key missing
            return {
                "score": 3.0,
                "max_score": 4.0,
                "rubric_match": 75,
                "presentation": f"Use a blue marker (605) to highlight key terms. Break paragraphs into crisp 2-line points with bullet symbols.",
                "diagrams": "Draw a circular hand-drawn diagram illustrating the key structure, labeling at least three parts on the right hand side.",
                "corrections": f"The definition is correct but missing the secondary equation or core diagrammatic structure. (Error: {str(e)})"
            }

    def analyze_topic(self, subject, topic, board, grade):
        """Generates mock Board expected questions for a syllabus topic using Gemini."""
        try:
            prompt = (
                f"Subject: {subject}\n"
                f"Topic: {topic}\n"
                f"Board: {board}\n"
                f"Grade Level: {grade}"
            )

            system_prompt = get_topic_analyzer_system_prompt(subject, board, grade)

            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={"response_mime_type": "application/json"}
            )

            response = model.generate_content(f"{system_prompt}\n\n{prompt}")

            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif clean_text.startswith("```"):
                clean_text = clean_text.split("```")[1].split("```")[0].strip()

            return json.loads(clean_text)

        except Exception as e:
            return {
                "long_question": f"Explain the complete theoretical process of {topic} in detail along with essential diagrams and structural flow.",
                "short_questions": f"1. Define the fundamental principles of {topic}.\n2. List two practical applications of {topic} in modern industry.",
                "presentation_flow": f"Start with a definition block -> Flow diagram -> Formula list -> Detailed head-by-head description. (Error: {str(e)})"
            }
