#!/usr/bin/env python

# author Huy
# date 10/23/2019

from django.db import models

from api.models import Profile, TimeStampedModel, Lunchdate


class Lunch(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='lunch_profile')
    date = models.ForeignKey(Lunchdate, on_delete=models.CASCADE, related_name='lunch_date')
