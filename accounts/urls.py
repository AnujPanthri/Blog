from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',views.edit_profile, name='edit_profile'),
]
