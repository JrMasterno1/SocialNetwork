
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like/<str:id>", views.like, name="like"),
    path("user/<str:id>", views.user, name="user"),
    path("comment/<str:id>", views.comment, name="comment")
]
