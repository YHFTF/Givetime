from django.urls import path
from . import views

urlpatterns = [
    # 게시판 목록 (post_list) - 4개 게시판 공통
    path('<str:post_type>/', views.post_list, name='post_list'),

    # 게시글 상세 (post_detail) - 4개 게시판 공통
    path('<str:post_type>/<int:post_id>/', views.post_detail, name='post_detail'),

    # 게시글 작성
    path('<str:post_type>/create/', views.post_create, name='post_create'),

    # 게시글 수정
    path('<str:post_type>/<int:post_id>/update/', views.post_update, name='post_update'),

    # 게시글 삭제
    path('<str:post_type>/<int:post_id>/delete/', views.post_delete, name='post_delete'),

    # 댓글 작성
    path('<str:post_type>/<int:post_id>/comment/', views.add_comment, name='add_comment'),

    # 댓글 삭제
    path('<str:post_type>/<int:post_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
