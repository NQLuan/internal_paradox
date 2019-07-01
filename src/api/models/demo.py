from django.db import models
from api.models.timestamped import TimeStampedModel


class Demo(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    text = models.CharField(default='text demo', max_length=255)

    class Meta:
        db_table = 'demo'
