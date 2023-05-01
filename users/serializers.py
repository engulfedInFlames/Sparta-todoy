from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import ParseError

from .models import CustomUser


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password",
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get("password", None)

        if password is None:
            raise ParseError("Password is required.")

        user.set_password(password)
        user.save()

        return user


class UserSerializer(ModelSerializer):
    lists = SerializerMethodField()
    tasks = SerializerMethodField()

    def get_lists(self, user):
        return user.lists.all().count()

    def get_tasks(self, user):
        return user.tasks.all().count()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "nickname",
            "lists",
            "tasks",
            "is_staff",
            "is_active",
        )
        """
        extra_kwargs = {
            "password": {
                "read_only": True,
            }
        }
        """


class UserDetailSerializer(ModelSerializer):
    lists = SerializerMethodField()
    tasks = SerializerMethodField()

    def get_lists(self, user):
        return user.lists.values("title")

    def get_tasks(self, user):
        return user.tasks.values("content")

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "nickname",
            "lists",
            "tasks",
            "is_staff",
            "is_active",
            "last_login",
            "date_joined",
        )
        extra_kwargs = {
            "email": {
                "read_only": True,
            },
            "is_staff": {
                "read_only": True,
            },
        }

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
