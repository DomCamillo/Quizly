from django import views
from rest_framework.views import APIView
from ..models import Qiuz, Question


class QuizListView(APIView):
    def get(self, request):
        quiz = Qiuz.objetcts.all()
        return quiz