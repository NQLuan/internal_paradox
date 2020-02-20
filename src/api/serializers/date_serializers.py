#!/usr/bin/env python

# author Huy
# date 9/7/2019
from rest_framework import serializers

from api.models import Date


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ('id', 'profile', 'date', 'title', 'content', 'reason', 'type')
