from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError

from .models import Poll, Question, PossibleAnswer, Answer
from .permissions import AdminOrReadOnly, OwnerOrReadOnly
from .serializers import (
    PollSerializer, QuestionSerializer, PossibleAnswerSerializer, AnswerSerializer
)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.prefetch_related(
        'questions',
        'questions__possible_answers'
    ).all()
    serializer_class = PollSerializer
    permission_classes = (AdminOrReadOnly, )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related(
        'poll',
    ).prefetch_related(
        'possible_answers',
    ).all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser, )


class PossibleAnswerViewSet(viewsets.ModelViewSet):
    queryset = PossibleAnswer.objects.select_related('question').all()
    serializer_class = PossibleAnswerSerializer
    permission_classes = (IsAdminUser)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.select_related(
        'user',
        'question'
    ).prefetch_related(
        'possible_answer',
    ).all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, OwnerOrReadOnly)

    def create(self, request, question_id):
        def validate_type_answer(request_data, question_type):
            text_answer = request_data.get('text_answer')
            possible_answer = request_data.get('possible_answer')

            if question_type == 1 and not text_answer:
                raise ValidationError("Вопрос подразумевает текстовый ответ!")

            if question_type in [2, 3] and not possible_answer:
                raise ValidationError("Не выбра ни один вариант ответа!")

        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        question = get_object_or_404(Question, id=question_id)
        question_type = question.question_type

        validate_type_answer(request_data, question_type)

        if serializer.is_valid():
            try:
                serializer.save(user=request.user, question=question)
            except IntegrityError:
                raise ValidationError("Вы уже отвечали на этот вопрос!")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        obj = self.queryset.filter(user=request.user, question=question)
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)

