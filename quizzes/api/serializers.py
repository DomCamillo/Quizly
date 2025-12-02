from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Quiz, Question

class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']
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


class CreateQuizSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)

    def validate_url(self, value):
        """Validiere YouTube URL"""
        if 'youtube.com' not in value and 'youtu.be' not in value:
            raise serializers.ValidationError("Must be a valid YouTube URL")
        return value
