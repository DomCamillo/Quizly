from django.contrib import admin
from .models import Quiz, Question


class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status', 'created_at')
    search_fields = ('title', 'user__username', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_title', 'quiz', 'correct_answer', 'order']
    list_filter = ['quiz', 'correct_answer']
    search_fields = ['question_title']
    ordering = ['quiz', 'order']


admin.site.register(Question)
admin.site.register(Quiz)
