from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("post/", views.post_list, name="post_list"),
    path("post/<str:post_id>/", views.detail, name="detail"),
    path("new_something_url/", views.new_url_view, name="new_url"),
    path("old_url/", views.old_url_redirect, name="old_url"),
]