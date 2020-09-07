from django.db import models
import uuid

from api_base.models import TimeStampedModel


class TypeOff(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, null=True)
    label = models.CharField(max_length=255, null=True)
    descriptions = models.TextField()
    add_sub_day_off = models.IntegerField(default=0)

    class Meta:
        db_table = 'hr_type_off'