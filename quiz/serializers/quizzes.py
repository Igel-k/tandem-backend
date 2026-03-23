from rest_framework import serializers
from quiz.models.quizzes import Quiz, CodeCompletionQuestion, AsyncSorterQuestion, SingleChoiceQuestion, TrueFalseQuestion 

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

    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ('id', 'type', 'difficulty', 'section', 'time_limit', 'title', 'description', 'tags', 'questions_count')

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

    def get_questions_count(self, obj):
        questions = obj.get_questions()
        return questions.count() if questions is not None else 0


class SingleChoiceQuestionSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()

    class Meta:
        model = SingleChoiceQuestion
        fields = ('id', 'text', 'options')

    def get_text(self, obj):
        return {
            'ru': obj.text_ru,
            'en': obj.text_en
        }

    def get_options(self, obj):
        return [
            {
                "id": "a",
                "text": {
                    "ru": obj.option_a_ru,
                    "en": obj.option_a_en
                }
            },
            {
                "id": "b",
                "text": {
                    "ru": obj.option_b_ru,
                    "en": obj.option_b_en
                }
            },
            {
                "id": "c",
                "text": {
                    "ru": obj.option_c_ru,
                    "en": obj.option_c_en
                }
            },
            {
                "id": "d",
                "text": {
                    "ru": obj.option_d_ru,
                    "en": obj.option_d_en
                }
            }
        ]


class TrueFalseQuestionSerializer(serializers.ModelSerializer):
    statement = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()

    class Meta:
        model = TrueFalseQuestion
        fields = ('id', 'statement', 'explanation')

    def get_statement(self, obj):
        return {
            'ru': obj.statement_ru,
            'en': obj.statement_en
        }

    def get_explanation(self, obj):
        if not obj.explanation_ru and not obj.explanation_en:
            return None
        return {
            'ru': obj.explanation_ru or "",
            'en': obj.explanation_en or ""
        }


class QuizDetailSerializer(QuizListSerializer):
    questions = serializers.SerializerMethodField()

    class Meta(QuizListSerializer.Meta):
        fields = ('id', 'type', 'difficulty', 'section', 'time_limit', 'title', 'tags', 'questions_count', 'questions')

    def get_questions(self, obj):
        questions = obj.get_questions()
        
        if not questions:
            return []

        quiz_type_name = obj.quiz_type.name.strip().lower().replace("_", " ")
        
        if quiz_type_name == 'code completion':
            return CodeCompletionQuestionSerializer(questions, many=True).data
        elif quiz_type_name == 'async sorter':
            return AsyncSorterQuestionSerializer(questions, many=True).data
        elif quiz_type_name == 'single choice':
            return SingleChoiceQuestionSerializer(questions, many=True).data
        elif quiz_type_name == 'true false':
            return TrueFalseQuestionSerializer(questions, many=True).data
            
        return []