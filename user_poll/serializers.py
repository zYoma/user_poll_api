from rest_framework import serializers

from .models import Poll, Question, PossibleAnswer, Answer


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username', required=False)
    question = serializers.ReadOnlyField(source='question.text', required=False)

    class Meta:
        fields = ('__all__')
        model = Answer

    def validate(self, data):
        """
        Проверяем что ответ на вопрос соответсвует типу вопроса.
        """
        text_answer = data.get('text_answer')
        possible_answer = data.get('possible_answer')

        if not any([possible_answer, text_answer]):
            raise serializers.ValidationError("Нужно указать ответ!")

        return data


class PossibleAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = PossibleAnswer


class QuestionSerializer(serializers.ModelSerializer):
    possible_answers = PossibleAnswerSerializer(many=True)

    class Meta:
        fields = ('__all__')
        model = Question


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        fields = ('__all__')
        model = Poll
        read_only_fields = ('start_date',)
