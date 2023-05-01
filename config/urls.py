from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("lists/", include("lists.urls")),
    path("tasks/", include("tasks.urls")),
]
