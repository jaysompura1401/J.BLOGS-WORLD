from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('search/', views.search, name='search'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('follow/<str:username>/', views.follow_view, name='follow_view'),
]
