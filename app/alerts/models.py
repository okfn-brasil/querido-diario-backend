from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

User = get_user_model()


class Alert(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_string = models.CharField(max_length=255)
    territories = ArrayField(
        models.CharField(
            max_length=7,
        ),
        blank=True,
        null=True,
    )
    sub_themes = ArrayField(
        models.CharField(
            max_length=50,
        ),
        blank=True,
        null=True,
    )
    gov_entities = ArrayField(
        models.CharField(
            max_length=50,
        ),
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
