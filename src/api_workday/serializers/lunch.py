#!/usr/bin/env python

# author Huy 
# date 10/23/2019

from rest_framework import serializers

from api_workday.models import Lunch


class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = ('id', 'profile', 'date')
