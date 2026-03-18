import django_filters
from quiz.models.quizzes import Quiz

class QuizFilter(django_filters.FilterSet):
    difficulty = django_filters.NumberFilter(field_name='difficulty__level')
    quiz_type = django_filters.CharFilter(field_name='quiz_type__name')
    section = django_filters.CharFilter(field_name='section__name')

    class Meta:
        model = Quiz
        fields = ['difficulty', 'quiz_type', 'section']