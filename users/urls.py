from django.urls import path

from . import views


urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.Me.as_view(), name="me"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
]
