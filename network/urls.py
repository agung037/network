
from django.urls import path

from . import views

urlpatterns = [
    path("home/<str:route>/", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/view/<str:username>/", views.profile, name="profile"),
    path("profile/edit/<str:username>/", views.edit_profile, name="edit_profile"),
    path("following/", views.following_post, name="following_post"),
    path("comment/", views.comment, name="comment"),
    path("edit_post/", views.edit_post, name="edit_post"),
    path("get_with_ajax/", views.get_with_ajax, name="get_with_ajax"),
    path("follow_with_ajax/", views.follow_with_ajax, name="follow_with_ajax"),
    path("edit_post_with_ajax/", views.edit_post_with_ajax, name="edit_post_with_ajax"),
    path("like/", views.like, name="like"),


]
