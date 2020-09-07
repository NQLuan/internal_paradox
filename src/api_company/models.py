from django.db import models
import uuid

from api_base.models import TimeStampedModel


class Company(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, null=True)
    logo = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    descriptions = models.TextField()
    maximum_level_approved = models.IntegerField(default=2)

    class Meta:
        db_table = 'hr_company'