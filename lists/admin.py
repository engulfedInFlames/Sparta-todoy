from django.contrib import admin

from .models import List


@admin.register(List)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title",)
