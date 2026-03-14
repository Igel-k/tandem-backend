from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Section title')

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        db_table = 'quiz"."section'

    def __str__(self):
        return self.name

class Difficulty(models.Model):
    level = models.PositiveSmallIntegerField(unique=True, verbose_name='Difficulty level number')
    description = models.CharField(max_length=50, verbose_name='Difficulty level text', blank=True)

    class Meta:
        verbose_name = 'Difficulty'
        verbose_name_plural = 'Difficulties'
        ordering = ['level']
        db_table = 'quiz"."difficulty'

    def __str__(self):
        return str(self.level)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Tag title')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'quiz"."tag'

    def __str__(self):
        return self.name

class QuizType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Quiz title')
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='Description')

    class Meta:
        verbose_name = 'Quiz Type'
        verbose_name_plural = 'Quiz Types'
        db_table = 'quiz"."quiz_type'

    def __str__(self):
        return self.name