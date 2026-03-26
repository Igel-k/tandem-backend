from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from quiz.models.interactions import FavoriteQuiz
from quiz.models.quizzes import Quiz

class QuizFavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        favorite, created = FavoriteQuiz.objects.get_or_create(user=request.user, quiz=quiz)

        if not created:
            favorite.delete()
            return Response({"status": "removed", "is_favorite": False}, status=status.HTTP_200_OK)

        return Response({"status": "added", "is_favorite": True}, status=status.HTTP_201_CREATED)