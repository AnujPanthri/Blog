from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('add_post/', views.PostCreateView, name='add_post'),
    path('detail/<slug>/', views.PostDetailView, name='detail'),
    path('like/', views.likePost, name='like'),
]