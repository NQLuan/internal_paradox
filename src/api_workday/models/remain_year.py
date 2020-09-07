from django.db import models
import uuid

from api_base.models import TimeStampedModel
from api_user.models import Profile


class RemainYear(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    year = models.CharField(max_length=255, null=True)
    bonus = models.IntegerField()
    annual_leave = models.IntegerField()

    class Meta:
        db_table = 'hr_remain_year'