from django.db import models

from api_base.models import TimeStampedModel


class Team(TimeStampedModel):
    team_name = models.CharField(max_length=255)
    team_email = models.EmailField(max_length=255)
    team_leader = models.IntegerField(null=True)

    class Meta:
        db_table = 'hr_teams'
