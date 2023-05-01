from django.urls import path

from . import views

urlpatterns = [
    path("", views.Lists.as_view()),
    path("<int:id>/", views.ListDetail.as_view()),
    path("<int:id>/tasks/", views.CreateTask.as_view()),
]
