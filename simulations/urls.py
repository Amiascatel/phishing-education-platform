from django.urls import path
from . import views

app_name = 'simulations'

urlpatterns = [
    path('', views.simulation_list, name='simulation_list'),
    path('start/<int:template_id>/', views.start_simulation, name='start_simulation'),
    path('<uuid:simulation_id>/', views.run_simulation, name='run_simulation'),
    path('<uuid:simulation_id>/submit/', views.submit_simulation, name='submit_simulation'),
    path('<uuid:simulation_id>/result/', views.simulation_result, name='simulation_result'),
    path('history/', views.simulation_history, name='simulation_history'),
]
