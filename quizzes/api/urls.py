from django.contrib import admin
from django.urls import path, include
from .views import QuizListView, QuizCreateFromVideoView, QuizDetailView

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('createQuiz/', QuizCreateFromVideoView.as_view(), name='quiz-create-from-video'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
]