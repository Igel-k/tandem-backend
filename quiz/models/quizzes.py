from django.db import models
from .core import Section, Difficulty, Tag, QuizType

class Quiz(models.Model):
    quiz_type = models.ForeignKey(QuizType, on_delete=models.PROTECT, related_name='quizzes', verbose_name='Quiz type')
    difficulty = models.ForeignKey(Difficulty, on_delete=models.PROTECT, related_name='quizzes', verbose_name='Difficulty')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='quizzes', verbose_name='Section')
    
    title_ru = models.CharField(max_length=200, verbose_name='Title (RU)')
    title_en = models.CharField(max_length=200, verbose_name='Title (EN)')
    
    tags = models.ManyToManyField(Tag, related_name='quizzes', verbose_name='Tags', blank=True)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        db_table = 'quiz"."quiz'

    def __str__(self):
        return f"Квиз {self.id} - {self.title_ru}"


class CodeCompletionQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='code_completion_questions', verbose_name='Quiz')
    
    code = models.TextField(verbose_name='Code')
    blanks = models.CharField(max_length=100, verbose_name='Blanks')
    
    correct_answer = models.CharField(max_length=255, verbose_name='Answer')
    
    hint_ru = models.TextField(verbose_name='Hint (RU)', blank=True, null=True)
    hint_en = models.TextField(verbose_name='Hint (EN)', blank=True, null=True)

    class Meta:
        verbose_name = 'Question Code Completion'
        verbose_name_plural = 'Questions Code Completion'
        ordering = ['id']
        db_table = 'quiz"."code_completion_question'

    def __str__(self):
        return f"Вопрос {self.order} для квиза {self.quiz.id}"


class AsyncSorterQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='async_sorter_questions', verbose_name='Quiz')
    
    code = models.TextField(verbose_name='Code')
    blocks = models.JSONField(default=list, verbose_name='Blocks')
    
    correct_sequence = models.JSONField(default=list, verbose_name='Answer')

    class Meta:
        verbose_name = 'Question Async Sorter'
        verbose_name_plural = 'Questions Async Sorter'
        ordering = ['id']
        db_table = 'quiz"."async_sorter_question'

    def __str__(self):
        return f"Вопрос {self.order} для квиза {self.quiz.id}"