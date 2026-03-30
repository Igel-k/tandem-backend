import django_filters
from quiz.models.quizzes import Quiz
from quiz.models.interactions import QuizResult

class QuizFilter(django_filters.FilterSet):
    difficulty = django_filters.NumberFilter(field_name='difficulty__level')
    quiz_type = django_filters.CharFilter(field_name='quiz_type__name')

    section = django_filters.CharFilter(method='filter_section')
    is_perfect = django_filters.BooleanFilter(method='filter_is_perfect')

    class Meta:
        model = Quiz
        fields = ['difficulty', 'quiz_type', 'section', 'is_perfect']

    def filter_section(self, queryset, name, value):
        if value.lower() == 'favorites':
            user = getattr(self, 'request', None) and self.request.user
            
            if user and user.is_authenticated:
                return queryset.filter(favorited_by__user=user)
            else:
                return queryset.none()

        return queryset.filter(section__name=value)

    def filter_is_perfect(self, queryset, name, value):
        user = getattr(self, 'request', None) and self.request.user
        
        if user and user.is_authenticated:
            perfect_quiz_ids = QuizResult.objects.filter(
                user=user, 
                score__gte=70
            ).values_list('quiz_id', flat=True)
            
            if value is True:
                return queryset.filter(id__in=perfect_quiz_ids)
            elif value is False:
                return queryset.exclude(id__in=perfect_quiz_ids)
                
        if value is True:
            return queryset.none()
            
        return queryset