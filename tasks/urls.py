from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>/", views.TaskDetail.as_view()),
    path("<int:id>/complete/", views.ToggleCompletedOrNot.as_view()),
]
