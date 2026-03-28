from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommentListCreateView.as_view(), name='comment-iist'),
    path('<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('my-comments/', views.MyCommentView.as_view(), name='my-comments'),
    path('post/<int:post_id>', views.post_comments, name = 'post-comments'),
    path('post/<int:post_id>/replies/', views.comment_replies, name='comment-replies'),
]