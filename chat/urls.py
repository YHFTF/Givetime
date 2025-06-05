from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('<str:nickname>/', views.room, name='room'),
]
