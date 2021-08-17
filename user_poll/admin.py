from django.contrib import admin
from . models import Poll, Question, PossibleAnswer, Answer


class PollAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question_type', 'poll']


class PossibleAnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'user']


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(PossibleAnswer, PossibleAnswerAdmin)
