from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.my_page, name='my_page'),
    path('update/<int:user_id>/', views.update_profile, name='update_profile'),
]
