#!/usr/bin/env python

# author OS
# date 7/25/2019

from django.conf import settings

from api_base.services import BaseService
from api_user.models import Profile, User
from api_user.serializers import ProfileSerializers


class TeamService(BaseService):

    @classmethod
    def list_team_member(cls, serializer_data):
        leaders = Profile.objects.select_related('user').values('user_id', 'user__active', 'teams', 'name')
        return [cls.get_profile(i, i['id'], leaders) for i in serializer_data]

    @classmethod
    def retrieve_team_member(cls, serializer_data, instance):
        leaders = Profile.objects.select_related('user').filter(user_id=instance.team_leader).values(
            'user_id', 'user__active', 'teams', 'name')
        return {
            "team": cls.get_profile(serializer_data, instance.id, leaders)
        }

    @classmethod
    def add_new_member(cls, data, instance):
        user = User.objects.get(email=data['email'])
        cls.update_user_team(user.id, instance.id)

    @classmethod
    def update_leader_teams(cls, data):
        leader_id = data['team_leader']
        team_id = data['id']
        cls.update_user_team(leader_id, team_id)

    @classmethod
    def remove_member(cls, data, instance):
        user = User.objects.get(email=data['email'])
        cls._remove_team(user.profile, instance.id)
        user.profile.save()

    @classmethod
    def remove_team(cls, team):
        members = Profile.objects.filter(teams__contains=team.id)
        for member in members:
            cls._remove_team(member, team.id)
        members.bulk_update(members, ['teams'])

    @classmethod
    def get_leader(cls):
        users = User.objects.select_related('profile').values('id', 'email', 'profile__name').filter(active=1)
        return [{
            'id': user['id'],
            'email': user['email'],
            'name': user['profile__name']
        } for user in users]

    @classmethod
    def get_potential_members(cls, instance):
        profiles = Profile.objects.select_related('user').filter(user__active=1).exclude(
            teams__regex=r'(^|,)' + str(instance.id) + '(,|$)').values('name', 'user__email')
        return [{
            'name': profile['name'],
            'email': profile['user__email']
        } for profile in profiles]

    @classmethod
    def get_profile(cls, data, pk, leaders):
        check = True
        data["leader_name"] = "No leader"
        if data["team_leader"]:
            for leader in leaders:
                if cls.leader_accept(data, leader):
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

    @classmethod
    def leader_accept(cls, data, leader):
        return data["team_leader"] == leader['user_id'] and leader['user__active'] and leader['teams'] \
               and str(data['id']) in leader['teams'].split(',')

    @classmethod
    def update_user_team(cls, user_id, team_id):
        user = Profile.objects.get(user=user_id)
        if user.teams:
            user.teams = str(team_id) + "," + user.teams
        else:
            user.teams = str(team_id)
        user.save()

    @classmethod
    def _remove_team(cls, member, team_id):
        member.teams = (',' + member.teams + ',').replace(',' + str(team_id) + ',', ',')[1:-1]
        if member.teams == "":
            member.teams = None
