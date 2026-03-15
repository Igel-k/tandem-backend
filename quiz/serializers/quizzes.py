from rest_framework import serializers
from quiz.models.quizzes import Quiz, CodeCompletionQuestion, AsyncSorterQuestion

class CodeCompletionQuestionSerializer(serializers.ModelSerializer):
    hint = serializers.SerializerMethodField()

    class Meta:
        model = CodeCompletionQuestion
        fields = ('id', 'code', 'blanks', 'hint')

    def get_hint(self, obj):
        if not obj.hint_ru and not obj.hint_en:
            return None
        return {
            'ru': obj.hint_ru or "",
            'en': obj.hint_en or ""
        }


class AsyncSorterQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsyncSorterQuestion
        fields = ('id', 'code', 'blocks')


class QuizListSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='quiz_type.name')
    difficulty = serializers.IntegerField(source='difficulty.level')
    section = serializers.CharField(source='section.name')
    
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ('id', 'type', 'difficulty', 'section', 'time_limit', 'title', 'description', 'tags')

    def get_title(self, obj):
        return {
            'ru': obj.title_ru,
            'en': obj.title_en
        }

    def get_description(self, obj):
        return {
            'ru': obj.description_ru,
            'en': obj.description_en
        }

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class QuizDetailSerializer(QuizListSerializer):
    questions = serializers.SerializerMethodField()

    class Meta(QuizListSerializer.Meta):
        fields = ('id', 'type', 'difficulty', 'section', 'time_limit', 'title', 'tags', 'questions')

    def get_questions(self, obj):
        quiz_type_name = obj.quiz_type.name.strip().lower().replace("_", " ")
        
        if quiz_type_name == 'code completion':
            questions = obj.code_completion_questions.all()
            return CodeCompletionQuestionSerializer(questions, many=True).data
            
        elif quiz_type_name == 'async sorter':
            questions = obj.async_sorter_questions.all()
            return AsyncSorterQuestionSerializer(questions, many=True).data
            
        return []