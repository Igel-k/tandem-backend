from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from quiz.models.quizzes import Quiz
from quiz.models.interactions import QuizResult
from quiz.serializers.quizzes import QuizListSerializer, QuizDetailSerializer
from quiz.filters.quizzes import QuizFilter
from rest_framework.permissions import IsAuthenticated
from quiz.services.grading import calculate_quiz_score

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

class QuizSubmitView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        answers_list = request.data.get('answers', [])
        
        if not isinstance(answers_list, list):
            return Response({"error": "Поле answers должно быть массивом"}, status=status.HTTP_400_BAD_REQUEST)

        grading_result = calculate_quiz_score(quiz, answers_list)
        
        if "error" in grading_result:
            return Response({"error": grading_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=grading_result["score"]
        )

        return Response({
            "quiz_id": quiz.id,
            "score": round(grading_result["score"], 2),
            "correct_count": grading_result["correct_count"],
            "total_questions": grading_result["total_questions"],
            "results": grading_result["results"]
        }, status=status.HTTP_200_OK)