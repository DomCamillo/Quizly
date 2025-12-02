from django.db import models
from django.contrib.auth.models import User



class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(max_length=200, blank=True, null=True )
    status = models.CharField(max_length=20, choices=[('processing','Processing'),
                                                      ('completed', 'Completed'),
                                                      ('failed', 'Failed')], default='processing')
    transcript = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Qiuz'

def __str__(self):
    return self.title




class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=500)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer =models.CharField(max_length=1, choices=[
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D'),
        ])
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['order']

    def __str__(self):
        return f"{self.question_title} – {self.quiz.title[:50]}"

