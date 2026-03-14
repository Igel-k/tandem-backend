from rest_framework import generics
from quiz.models.quizzes import Quiz
from quiz.serializers.quizzes import QuizListSerializer, QuizDetailSerializer

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    permission_classes = [] 

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = []