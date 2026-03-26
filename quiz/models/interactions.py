from django.db import models
from django.conf import settings
from .quizzes import Quiz

class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_results', verbose_name='User')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results', verbose_name='Quiz')
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Percentage')

    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Completed date')

    class Meta:
        verbose_name = 'Quiz result'
        verbose_name_plural = 'Quizzes results'
        db_table = 'quiz"."quiz_result'
        ordering = ['-completed_at'] 

    def __str__(self):
        return f"{self.user} - {self.quiz.title_ru} ({self.score}%)"


class FavoriteQuiz(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_quizzes', verbose_name='User')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Quiz')
    
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Adding date')

    class Meta:
        verbose_name = 'Favorite quiz'
        verbose_name_plural = 'Favorites quizzes'
        db_table = 'quiz"."favorite_quiz'
        unique_together = ('user', 'quiz') 

    def __str__(self):
        return f"{self.user} -> {self.quiz.title_ru}"
