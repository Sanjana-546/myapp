from django.urls import path

from . import api_views, views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('post/', views.post_list, name='post_list'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.detail, name='detail'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:user_id>/', views.author_detail, name='author_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('new_something_url/', views.new_url_view, name='new_url'),
    path('old_url/', views.old_url_redirect, name='old_url'),
    # JWT Authentication API endpoints
    path('api/token/', api_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', api_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', api_views.custom_token_verify, name='token_verify'),
    path('api/protected/', api_views.protected_view, name='protected'),
]
