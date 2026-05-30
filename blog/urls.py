from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
