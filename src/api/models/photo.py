#!/usr/bin/env python

# author Huy
# date 9/17/2019
from django.db import models

from api.models import Profile, TimeStampedModel


def name_file(instance, filename):
    return '/'.join(['images', str(instance.profile.id), filename])


class Photo(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photo')
    photo = models.ImageField(upload_to=name_file, max_length=255, blank=True, null=True)
