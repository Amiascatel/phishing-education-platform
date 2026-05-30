from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # Category pages
    path('', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/<slug:slug>/start/', views.start_quiz, name='start_quiz'),

    # Quiz session & results
    path('attempt/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('profile/', views.knowledge_profile, name='knowledge_profile'),

    # Videos
    path('videos/', views.videos_list, name='videos_list'),
    path('videos/<int:video_id>/watched/', views.mark_video_watched, name='mark_video_watched'),

    # AJAX API
    path('api/answer/', views.api_submit_answer, name='api_submit_answer'),
    path('api/complete/', views.api_complete_quiz, name='api_complete_quiz'),

    # Chatbot
    path('api/chat/', views.chatbot_message, name='chatbot_message'),
]
