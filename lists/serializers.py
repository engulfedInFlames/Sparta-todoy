from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import List
from tasks.serializers import SimpleTaskSerializer


class CreateListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ("title",)


class ListsSerializer(ModelSerializer):
    tasks = SerializerMethodField()

    def get_tasks(self, list):
        return list.tasks.all().count()

    class Meta:
        model = List
        fields = (
            "id",
            "user",
            "title",
            "tasks",
        )


class ListDetailSerializer(ModelSerializer):
    tasks = SerializerMethodField()

    def get_tasks(self, list):
        _tasks = list.tasks.all()
        serializer = SimpleTaskSerializer(
            _tasks,
            many=True,
        )
        return serializer.data

    class Meta:
        model = List
        fields = (
            "id",
            "user",
            "title",
            "tasks",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "user": {
                "read_only": True,
            }
        }
