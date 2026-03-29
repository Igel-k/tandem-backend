from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from quiz.models.quizzes import Quiz
from quiz.models.interactions import QuizResult

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_tests = Quiz.objects.count()
        total_attempts = QuizResult.objects.filter(user=user).count()

        completed_tests_ids = set(QuizResult.objects.filter(user=user, score__gte=70).values_list('quiz_id', flat=True))
        completed_tests = len(completed_tests_ids)
        remain_tests = total_tests - completed_tests

        general_stats = {
            "testsCount": total_tests,
            "totalAttempts": total_attempts,
            "completedTests": completed_tests,
            "remainTests": remain_tests
        }

        sections_data = Quiz.objects.values('section__name').annotate(total=Count('id')).order_by('section__name')
        
        section_progress = []
        for sec in sections_data:
            theme_name = sec['section__name']
            
            completed_in_section = Quiz.objects.filter(
                id__in=completed_tests_ids, 
                section__name=theme_name
            ).count()
            
            section_progress.append({
                "theme": theme_name,
                "tests": sec['total'],
                "completedTestsCount": completed_in_section
            })


        difficulty_data = Quiz.objects.values('difficulty__level').annotate(total=Count('id')).order_by('difficulty__level')
        
        difficulty_progress = []
        for diff in difficulty_data:
            diff_level = diff['difficulty__level']
            
            completed_in_diff = Quiz.objects.filter(
                id__in=completed_tests_ids, 
                difficulty__level=diff_level
            ).count()
            
            difficulty_progress.append({
                "difficulty": diff_level,
                "tests": diff['total'],
                "completedTestsCount": completed_in_diff
            })

        return Response({
            "general": general_stats,
            "by_section": section_progress,
            "by_difficulty": difficulty_progress
        })