from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('pre-assessment/', views.pre_assessment, name='pre_assessment'),
    path('post-assessment/', views.post_assessment, name='post_assessment'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:attempt_id>/question/', views.quiz_question, name='quiz_question'),
    path('quiz/<int:attempt_id>/submit/', views.submit_answer, name='submit_answer'),
    path('quiz/<int:attempt_id>/complete/', views.complete_quiz, name='complete_quiz'),
    path('quiz/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
    path('results/', views.assessment_results, name='assessment_results'),
    path('history/', views.quiz_history, name='quiz_history'),
]
