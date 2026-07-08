from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home, name='home'),

    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/update/', views.post_update, name='post_update'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:post_id>/like/', views.post_like, name='post_like'),

    path('posts/<int:post_id>/comments/create/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_id>/reply/', views.reply_create, name='reply_create'),
    path('comments/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    path('stories/create/', views.story_create, name='story_create'),

    path('search/', views.user_search, name='user_search'),

    path('profile/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('profile/<str:username>/', views.profile, name='profile'),
]