from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('ping', views.test, name = 'test'),
    path('user/<str:username>', views.user, name = 'username'),
    path('user/<str:username>/repos', views.user_repos, name = 'username'),
]
