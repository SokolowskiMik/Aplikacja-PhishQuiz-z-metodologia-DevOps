from django.urls import path
from .views import quiz_view, check_answer_view

urlpatterns = [
    path('', quiz_view, name='quiz-page'),
    path('check-answer/', check_answer_view, name='check-answer'),
]