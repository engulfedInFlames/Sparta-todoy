from rest_framework.serializers import ModelSerializer

from .models import Task


class CreateTaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ("content",)


class TaskDetailSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "user",
            "list",
            "content",
            "is_completed",
            "created_at",
            "updated_at",
            "completed_at",
        )


class SimpleTaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "content",
            "is_completed",
            "created_at",
            "updated_at",
            "completed_at",
        )
