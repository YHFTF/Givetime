from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.my_page, name='my_page'),  # 내 마이페이지
    path('profile/<str:nickname>/', views.view_profile, name='view_profile'),  # 닉네임 기반 프로필 보기
    path('update/<int:user_id>/', views.update_profile, name='update_profile'),  # 프로필 수정
    path('search/', views.search_user, name='search_user'),  # 닉네임 검색
    path('register-admin/', views.register_admin, name='register_admin'),  # 관리자 등록
    path('admin/set-exp/', views.set_user_exp, name='set_user_exp'),  # EXP 변경
]
