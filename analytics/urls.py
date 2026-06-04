from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard, name='dashboard'),
    path('chart-data/', views.performance_chart_data, name='chart_data'),
    path('activity/', views.activity_feed, name='activity_feed'),
    path('dismiss-recommendation/<int:recommendation_id>/', views.dismiss_recommendation, name='dismiss_recommendation'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('skills/', views.skill_breakdown, name='skill_breakdown'),
]
