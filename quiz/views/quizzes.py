from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from quiz.models.quizzes import Quiz
from quiz.serializers.quizzes import QuizListSerializer, QuizDetailSerializer
from quiz.filters.quizzes import QuizFilter

class QuizListPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 20

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all().order_by('id')
    serializer_class = QuizListSerializer
    permission_classes = [] 
    pagination_class = QuizListPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuizFilter

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = []