#!/usr/bin/env python

# author Huy
# date 9/7/2019

from rest_framework import serializers

from api_workday.models import ProposeLeave


class ProposeLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposeLeave
        fields = ('id', 'profile', 'start', 'end', 'start_hour', 'end_hour', 'lunch', 'title', 'comments', 'status')
