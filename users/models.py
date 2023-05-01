from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The email is required."))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    class GenderKinds(models.TextChoices):
        MALE = ("male", "남성")
        FEMALE = ("female", "여성")

    username = None  # username 필드 제거
    email = models.EmailField(unique=True)
    nickname = models.CharField(
        max_length=120,
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=20,
        choices=GenderKinds.choices,
        null=True,
        blank=True,
    )
    age = models.PositiveBigIntegerField(null=True, blank=True)
    introduction = models.TextField(
        null=True,
        blank=True,
    )

    objects = CustomUserManager()

    """
    1.  USERNAME_FIELD는 User 모델에서 ID 부여의 기준이 된다. 이를 username이 아닌 email 필드로 설정.
    2. REQUIRED_FIELDS에는 USERNAME_FIELD로 설정된 필드가 있어서는 안 된다.
    """

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return str(self.email)
