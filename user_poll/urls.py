from django.urls import path, include
from .views import PollViewSet, QuestionViewSet, PossibleAnswerViewSet, AnswerViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('poll', PollViewSet)
router.register('question', QuestionViewSet)
router.register(r'question/(?P<question_id>\d+)/possible_answers', PossibleAnswerViewSet)
router.register(r'question/(?P<question_id>\d+)/answers', AnswerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]