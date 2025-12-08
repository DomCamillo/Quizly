import google.generativeai as genai
import json
from django.conf import settings


class QuizGenerator:
    """Generates quiz questions using Google Gemini AI"""

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)

        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_quiz_from_transcript(self, transcript, num_questions=5):
        """
        Generiert Quiz-Fragen aus einem Transkript
        Returns: List of dict mit question_data
        """
        prompt = f"""
Based on the following transcript, generate {num_questions} multiple-choice quiz questions.

Transcript:
{transcript}

Please respond with a JSON array containing exactly {num_questions} questions.
Each question should have this structure:
{{
    "question_title": "The question text",
    "option_a": "First option",
    "option_b": "Second option",
    "option_c": "Third option",
    "option_d": "Fourth option",
    "correct_answer": "A" (or B, C, D)
}}

IMPORTANT: Respond ONLY with valid JSON, no additional text.
"""

        response = self.model.generate_content(prompt)

        try:
            """parse response as JSON"""
            questions_data = json.loads(response.text)
            return questions_data
        except json.JSONDecodeError:
            """if gemini adds extra text try to extract JSON"""
            text = response.text
            """looking for first [ and last ] to extract JSON """
            start = text.find('[')
            end = text.rfind(']') + 1
            if start != -1 and end != 0:
                questions_data = json.loads(text[start:end])
                return questions_data
            raise ValueError("Could not parse quiz questions from AI response")