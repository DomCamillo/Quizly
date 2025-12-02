from django.contrib import admin
from django.urls import path, include
from .views import QuizListView

urlpatterns = [
    path('quizzes/',QuizListView.as_view(), name='quiz-list' ),

]
