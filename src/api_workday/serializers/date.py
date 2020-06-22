#!/usr/bin/env python

# author Huy
# date 9/7/2019

from rest_framework import serializers

from api_workday.constants import Workday
from api_workday.models import Date


class DateSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['class'] = {
            Workday.MORNING: 'Morning',
            Workday.AFTERNOON: 'Afternoon',
            Workday.FULL: 'Full'
        }[ret.get('type')]
        ret.update(
            start=ret.get('date'),
            end=ret.get('date')
        )
        return ret

    class Meta:
        model = Date
        fields = ('id', 'profile', 'date', 'title', 'content', 'reason', 'type')
