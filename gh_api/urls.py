from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("ping", views.test, name="test"),
    path("user/<str:username>", views.user, name="user"),
    path("user/<str:username>/repos", views.user_repos, name="user-repos"),
    path("user/<str:username>/trends", views.user_trends, name="user-trends"),
    path("user/<str:username>/stats", views.user_stats, name="user-stats"),
]
