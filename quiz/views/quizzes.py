from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from quiz.models.quizzes import Quiz
from quiz.serializers.quizzes import QuizListSerializer, QuizDetailSerializer

class QuizListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all().order_by('id')
    serializer_class = QuizListSerializer
    permission_classes = [] 
    pagination_class = QuizListPagination

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = []