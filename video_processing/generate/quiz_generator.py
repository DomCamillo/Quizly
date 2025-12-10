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
        Generates multiple-choice quiz questions from a transcript
        Returns: Dict with title, description, and questions
        """
        prompt = f"""
Based on the following transcript, generate {num_questions} multiple-choice quiz questions.

Transcript:
{transcript}

Please respond with a JSON object with this EXACT structure:
{{
    "description": "A brief 2-3 sentence description of what this quiz covers",
    "questions": [
        {{
            "question_title": "The question text",
            "option_a": "First option",
            "option_b": "Second option",
            "option_c": "Third option",
            "option_d": "Fourth option",
            "correct_answer": "A"
        }}
    ]
}}

Generate exactly {num_questions} questions in the "questions" array.
The description should summarize the main topics covered in the quiz.

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
            """looking for first { and last } to extract JSON """
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != 0:
                questions_data = json.loads(text[start:end])
                return questions_data
            raise ValueError("Could not parse quiz questions from AI response")