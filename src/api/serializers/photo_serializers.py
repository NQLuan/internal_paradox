#!/usr/bin/env python

# author Huy
# date 9/7/2019
from rest_framework import serializers

from api.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'profile', 'photo')
