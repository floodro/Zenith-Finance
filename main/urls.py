from django.urls import path
from . import views #import views.py from main

urlpatterns = [
    path("", views.index, name='main'),  # home page
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup')
]