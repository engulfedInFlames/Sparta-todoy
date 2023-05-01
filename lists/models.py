from django.db import models
from django.conf import settings

from common.models import CommonModel


class List(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lists",
    )

    title = models.CharField(
        max_length=160,
    )
