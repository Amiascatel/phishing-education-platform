from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('modules/', views.module_list, name='module_list'),
    path('modules/<slug:slug>/', views.module_detail, name='module_detail'),
    path('modules/<slug:slug>/lesson/<int:lesson_id>/', views.lesson_view, name='lesson'),
    path('modules/<slug:slug>/complete/', views.complete_module, name='complete_module'),
    path('indicators/', views.phishing_indicators, name='indicators'),
    path('resources/', views.resources_view, name='resources'),
]
