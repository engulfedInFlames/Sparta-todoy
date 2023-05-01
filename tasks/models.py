from django.db import models
from django.conf import settings

from common.models import CommonModel


class Task(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    list = models.ForeignKey(
        "lists.List",
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    content = models.TextField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
