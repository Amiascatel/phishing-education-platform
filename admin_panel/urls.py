from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.students, name='students'),
    path('students/<int:user_id>/', views.student_detail, name='student_detail'),
    path('students/<int:user_id>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:user_id>/delete/', views.delete_student, name='delete_student'),
    path('students/<int:user_id>/password/', views.change_student_password, name='change_student_password'),
    path('content/', views.content, name='content'),
    path('content/question/add/', views.add_question, name='add_question'),
    path('content/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('content/question/<int:question_id>/toggle/', views.toggle_question, name='toggle_question'),
    path('content/video/add/', views.add_video, name='add_video'),
    path('content/video/<int:video_id>/delete/', views.delete_video, name='delete_video'),
    path('ml/', views.ml_management, name='ml_management'),
    path('ml/submit-qa/', views.submit_chatbot_qa, name='submit_chatbot_qa'),
    path('ml/feed/', views.feed_to_model, name='feed_to_model'),
    path('ml/retrain-difficulty/', views.retrain_difficulty_model, name='retrain_difficulty_model'),
    path('api/stats/', views.api_platform_stats, name='api_stats'),
    path('content/module/add/', views.add_module, name='add_module'),
    path('content/module/<int:module_id>/toggle/', views.toggle_module, name='toggle_module'),
    path('content/module/<int:module_id>/delete/', views.delete_module, name='delete_module'),
    path('content/indicator/add/', views.add_indicator, name='add_indicator'),
    path('content/indicator/<int:indicator_id>/delete/', views.delete_indicator, name='delete_indicator'),
    # Edit existing content
    path('content/module/<int:module_id>/edit/', views.edit_module, name='edit_module'),
    path('content/question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('content/video/<int:video_id>/edit/', views.edit_video, name='edit_video'),
    path('content/indicator/<int:indicator_id>/edit/', views.edit_indicator, name='edit_indicator'),
    # Blog management
    path('blog/', views.blog_management, name='blog_management'),
    path('blog/post/add/', views.add_blog_post, name='add_blog_post'),
    path('blog/post/<int:post_id>/edit/', views.edit_blog_post, name='edit_blog_post'),
    path('blog/post/<int:post_id>/delete/', views.delete_blog_post, name='delete_blog_post'),
    path('blog/category/add/', views.add_blog_category, name='add_blog_category'),
    path('blog/category/<int:cat_id>/delete/', views.delete_blog_category, name='delete_blog_category'),
    path('admins/', views.create_admin_user, name='create_admin'),
    path('admins/<int:user_id>/edit/', views.edit_admin_user, name='edit_admin'),
    path('admins/<int:user_id>/delete/', views.delete_admin_user, name='delete_admin'),
    path('profile/', views.admin_profile, name='admin_profile'),
]
