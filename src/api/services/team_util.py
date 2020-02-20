#!/usr/bin/env python

# author Huy
# date 8/1/2019
from django.conf import settings

from api.models import Profile, User
from api.serializers import ProfileSerializers
from api.services import BaseService


class TeamUtil(BaseService):
    """
    GET TEAM MEMBER'S PROFILE UTILITY FOR LIST AND RETRIEVE METHOD
    """

    @staticmethod
    def get_profile(data, pk, leaders):
        check = True
        data["leader_name"] = "No leader"
        if data["team_leader"]:
            for leader in leaders:
                if TeamUtil.leader_accept(data, leader):
                    data["leader_name"] = leader['name']
                    check = False
                    break
        if check:
            data["team_leader"] = 0

        profiles = Profile.objects.filter(teams__regex=r'(^|,)' + str(pk) + '(,|$)').select_related('user')
        data["employee_number"] = profiles.count()
        profile_serializer = ProfileSerializers(profiles, many=True)
        for profile in profile_serializer.data:
            if profile.get('image'):
                profile['image'] = settings.MEDIA_IMAGE + profile.get('image')
            if profile['id'] == data['team_leader']:
                profile['role'] = 'Leader'
            else:
                profile['role'] = 'Member'
            profile['email'] = User.objects.get(id=profile.get('id')).email
        data["employee_list"] = profile_serializer.data
        return data

    @staticmethod
    def leader_accept(data, leader):
        return data["team_leader"] == leader['user_id'] and leader['user__active'] and leader['teams'] \
               and str(data['id']) in leader['teams'].split(',')

    """
    UPDATE MEMBER'S TEAMS FIELD UTILITY
    """

    @staticmethod
    def update_teams(user_id, team_id):
        leader = Profile.objects.get(user=user_id)
        if leader.teams:
            leader.teams = str(team_id) + "," + leader.teams
        else:
            leader.teams = str(team_id)
        leader.save()

    """
    REMOVE MEMBER'S TEAMS FIELD UTILITY
    """

    @staticmethod
    def remove_team(member, team_id):
        member.teams = (',' + member.teams + ',').replace(',' + str(team_id) + ',', ',')[1:-1]
        if member.teams == "":
            member.teams = None
