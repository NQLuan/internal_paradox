from django.db import models
import uuid

from api_base.models import TimeStampedModel
from api_workday.models.request_off import RequestOff
from api_user.models import Profile



class RequestDetail(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    comment = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    request_off_id = models.ForeignKey(RequestOff, on_delete=models.CASCADE, related_name='request_detail')
    approve_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='approve_id')

    class Meta:
        db_table = 'hr_request_detail'