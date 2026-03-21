from django.db import models
from .core import Section, Difficulty, Tag, QuizType

class Quiz(models.Model):
    quiz_type = models.ForeignKey(QuizType, on_delete=models.PROTECT, related_name='quizzes', verbose_name='Quiz type')
    difficulty = models.ForeignKey(Difficulty, on_delete=models.PROTECT, related_name='quizzes', verbose_name='Difficulty')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='quizzes', verbose_name='Section')
    time_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name='Time limit')
    
    title_ru = models.CharField(max_length=200, verbose_name='Title (RU)')
    title_en = models.CharField(max_length=200, verbose_name='Title (EN)')

    description_ru = models.TextField(verbose_name='Description (RU)')
    description_en = models.TextField(verbose_name='Description (EN)')
    
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


class SingleChoiceQuestion(models.Model):
    ANSWER_CHOICES = (
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='single_choice_questions', verbose_name='Quiz')
    
    text_ru = models.TextField(verbose_name='Title (RU)')
    text_en = models.TextField(verbose_name='Title (EN)')

    option_a_ru = models.CharField(max_length=255, verbose_name='Option A (RU)')
    option_a_en = models.CharField(max_length=255, verbose_name='Option A (EN)')
    
    option_b_ru = models.CharField(max_length=255, verbose_name='Option B (RU)')
    option_b_en = models.CharField(max_length=255, verbose_name='Option B (EN)')
    
    option_c_ru = models.CharField(max_length=255, verbose_name='Option C (RU)')
    option_c_en = models.CharField(max_length=255, verbose_name='Option C (EN)')
    
    option_d_ru = models.CharField(max_length=255, verbose_name='Option D (RU)')
    option_d_en = models.CharField(max_length=255, verbose_name='Option D (EN)')

    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, verbose_name='Correct answer')

    class Meta:
        verbose_name = 'Question Single Choice'
        verbose_name_plural = 'Questions Single Choice'
        ordering = ['id']
        db_table = 'quiz"."single_choice_question'

    def __str__(self):
        return f"Вопрос {self.id} для квиза {self.quiz.id}"


class TrueFalseQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='true_false_questions', verbose_name='Quiz')
    
    statement_ru = models.TextField(verbose_name='Statement (RU)')
    statement_en = models.TextField(verbose_name='Statement (EN)')
    
    correct_answer = models.BooleanField(verbose_name='Correct answer')
    
    explanation_ru = models.TextField(verbose_name='Explanation (RU)', blank=True, null=True)
    explanation_en = models.TextField(verbose_name='Explanation (EN)', blank=True, null=True)

    class Meta:
        verbose_name = 'Question True/False'
        verbose_name_plural = 'Questions True/False'
        ordering = ['id']
        db_table = 'quiz"."true_false_question'

    def __str__(self):
        return f"Вопрос {self.id} для квиза {self.quiz.id}"