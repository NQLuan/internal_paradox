#!/usr/bin/env python

# author Huy
# date 9/7/2019
from django.db import models

from api.models import Profile, TimeStampedModel


class ProposeLeave(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='leave', default=1)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    lunch = models.CharField(max_length=255, default='No')
    start_hour = models.CharField(max_length=255, null=True)
    end_hour = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, default='Pending')
    comments = models.CharField(max_length=255, null=True)
