from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Quiz, Question
from video_processing.services import VideoProcessingService

class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.SerializerMethodField()
    correct_answer = serializers.CharField(source='correct_answer')

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at','correct_answer']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_question_options(self, obj):
        return [obj.option_a, obj.option_b, obj.option_c, obj.option_d]

    def get_answer(self, obj):
        return f"Option {obj.correct_answer}"


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at',
                  'video_url', 'status', 'questions']
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']


class QuizUpdateSerializer(serializers.ModelSerializer):
    """Serializer for partial Quiz-Updates (PATCH)"""
    class Meta:
        model = Quiz
        fields = ['title', 'description']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False}}

    def validate_title(self, value):
        """Validiere Title"""
        if value and len(value.strip()) == 0:
            raise serializers.ValidationError("Title cannot be empty")
        return value

class CreateQuizSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    def validate_url(self, value):
        """Validiere YouTube URL"""
        if 'youtube.com' not in value and 'youtu.be' not in value:
            raise serializers.ValidationError("Must be a valid YouTube URL")
        return value
