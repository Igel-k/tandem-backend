from django.urls import path
from .views.quizzes import QuizListView, QuizDetailView, QuizSubmitView
from .views.interactions import QuizFavoriteToggleView
from .views.dashboard import UserDashboardView

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('<int:pk>/submit/', QuizSubmitView.as_view(), name='quiz_submit'),
    path('<int:pk>/favorite/', QuizFavoriteToggleView.as_view(), name='quiz_favorite_toggle'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
]