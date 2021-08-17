from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

QUESTION_TYPES = (
    (1, 'text'),
    (2, 'choice'),
    (3, 'multiple_choice'),
)


class Poll(models.Model):
    name = models.CharField("Название", max_length=300)
    start_date = models.DateTimeField("Дата начала опроса", auto_now_add=True)
    end_date = models.DateTimeField("Дата окончания опроса")
    description = models.TextField("Описание", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class Question(models.Model):
    text = models.TextField("Текст вопроса")
    question_type = models.IntegerField("Тип вопроса", choices=QUESTION_TYPES, default=1)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class PossibleAnswer(models.Model):
    text = models.TextField("Вариант ответа")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='possible_answers')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    possible_answer = models.ManyToManyField(PossibleAnswer, blank=True)
    text_answer = models.TextField("Текстовый ответ", blank=True, null=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        constraints = [
            models.UniqueConstraint(fields=['question', 'user'],  name='user_question')
        ]
