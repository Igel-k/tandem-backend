from django.urls import path
from .views.quizzes import QuizListView, QuizDetailView

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
]