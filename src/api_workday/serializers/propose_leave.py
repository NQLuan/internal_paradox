#!/usr/bin/env python

# author Huy
# date 9/7/2019
import json

from rest_framework import serializers

from api_team.models import Team
from api_user.models import Profile
from api_workday.constants import Workday
from api_workday.models import ProposeLeave
from api_workday.services import DateService


class ProposeLeaveSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        profile_id = ret.get('profile')
        profile = Profile.objects.get(id=profile_id)
        ret.update(
            name=profile.name,
            leave_day_left=DateService.get_leave_day_statistic(profile_id).get('leave_day_left'),
            team='No team',
            start_hour=Workday.DEFAULT_START_HOUR,
            end_hour=Workday.DEFAULT_END_HOUR
        )
        if profile.teams:
            team = Team.objects.filter(id=int(profile.teams.split(',')[0])).first()
            if team:
                ret.update(team=team.team_name)
        if ret.get('start_hour') and ret.get('end_hour'):
            start_hour_json = json.loads(ret.get('start_hour'))
            end_hour_json = json.loads(ret.get('end_hour'))
            start_hour = f"{start_hour_json.get('hour')}:{start_hour_json.get('min')}"
            end_hour = f"{end_hour_json.get('hour')}:{end_hour_json.get('min')}"
            ret.update(
                start_hour=start_hour,
                end_hour=end_hour
            )
        return ret

    class Meta:
        model = ProposeLeave
        fields = ('id', 'profile', 'start', 'end', 'start_hour', 'end_hour', 'lunch', 'title', 'comments', 'status')
