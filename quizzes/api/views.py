from django import views
from rest_framework.views import APIView
from ..models import Quiz, Question
from .serializers import QuizSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import QuizSerializer, CreateQuizSerializer, QuizUpdateSerializer
from video_processing.services import VideoProcessingService


class QuizListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Nur Quizzes des eingeloggten Users
        quizzes = Quiz.objects.filter(user=request.user)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class QuizCreateFromVideoView(APIView):
    """Erstellt ein Quiz aus einer YouTube URL"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateQuizSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        video_url = serializer.validated_data['url']
        quiz = Quiz.objects.create(
            user=request.user,
            video_url=video_url,
            title=f"Quiz from {video_url[:50]}...",
            status='processing'
        )
        try:
            VideoProcessingService.process_video_and_create_quiz(quiz.id)
        except Exception as e:
            quiz.status = 'failed'
            quiz.save()
            return Response(
                {'error': f'Processing failed: {str(e)}'},
                status=500
            )
        return Response(
            QuizSerializer(quiz).data,
            status=201
        )


class QuizDetailView(APIView):
    """Get single quiz for delete or update"""
    permission_classes = [IsAuthenticated]

    def get_quiz(self, pk, user):
        try:
            quiz = Quiz.objects.get(pk=pk)
            if quiz.user != user:
                return None, Response(
                    {'error': 'Access denied - Quiz does not belong to you'},
                    status=status.HTTP_403_FORBIDDEN
                )
            return quiz, None

        except Quiz.DoesNotExist:
            return None, Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        """GET: Einzelnes Quiz abrufen"""
        quiz, error_response = self.get_quiz(pk, request.user)
        if error_response:
            return error_response

        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def patch(self, request, pk):
        """PATCH: Quiz teilweise aktualisieren"""
        quiz, error_response = self.get_quiz(pk, request.user)
        if error_response:
            return error_response
        serializer = QuizUpdateSerializer(quiz, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            QuizSerializer(quiz).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        """DELETE: Quiz permanent löschen"""
        quiz, error_response = self.get_quiz(pk, request.user)
        if error_response:
            return error_response
        quiz.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )