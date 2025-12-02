from django import views
from rest_framework.views import APIView
from ..models import Quiz, Question
from .serializers import QuizSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class QuizListView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, 400)
        serializer.save()
        return Response(serializer.data, 201)



class CreateQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Validiere die URL
        serializer = QuizSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        youtube_url = serializer.validated_data['url']

        # 2. Erstelle Quiz-Objekt
        quiz = Quiz.objects.create(
            user=request.user,
            title=f"Test Quiz from {youtube_url[:30]}...",  # Dummy-Titel
            description="This is a test quiz generated from YouTube video",
            video_url=youtube_url,
            status='processing'  # Markiere als "in Bearbeitung"
        )

        # 3. TODO: Hier kommt später die Video-Verarbeitung
        # - YouTube Download mit yt_dlp
        # - Whisper Transkription
        # - Gemini Quiz-Generierung

        # 4. MOCK-DATEN zum Testen (später entfernen!)
        # Erstelle Test-Fragen
        mock_questions_data = [
            {
                "question_title": "Was ist die Hauptaussage des Videos?",
                "option_a": "Python ist die beste Programmiersprache",
                "option_b": "JavaScript ist schneller als Python",
                "option_c": "Django ist ein Web-Framework",
                "option_d": "Alle Antworten sind richtig",
                "correct_answer": "C",
                "order": 1
            },
            {
                "question_title": "Welche Technologie wurde im Video erwähnt?",
                "option_a": "React",
                "option_b": "Vue.js",
                "option_c": "Angular",
                "option_d": "Django REST Framework",
                "correct_answer": "D",
                "order": 2
            },
            {
                "question_title": "Was ist ein API Endpoint?",
                "option_a": "Eine Datenbank",
                "option_b": "Eine URL für API-Anfragen",
                "option_c": "Ein Frontend-Framework",
                "option_d": "Eine Programmiersprache",
                "correct_answer": "B",
                "order": 3
            }
        ]

        # Erstelle Mock-Questions
        for q_data in mock_questions_data:
            Question.objects.create(
                quiz=quiz,
                **q_data
            )

        # 5. Setze Status auf "completed"
        quiz.status = 'completed'
        quiz.save()

        # 6. Serialize und sende Response
        response_serializer = QuizSerializer(quiz)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)