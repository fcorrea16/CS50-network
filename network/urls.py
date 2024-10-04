from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),

    # API routes
    path("post/<int:post_id>", views.post, name="post"),
    path("like/<int:like_id>", views.like, name="like"),
]
