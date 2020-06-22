#!/usr/bin/env python

# author OS
# date 7/25/2019

from api_base.services import BaseService
from api_user.models import Profile, User
from api_user.serializers.profile import TeamProfile
from api_user.services import UserService


class TeamService(BaseService):

    @classmethod
    def add_new_member(cls, instance, **kwargs):
        user = UserService.get_user_by_email(kwargs.get('email'))
        if user:
            cls.update_user_team(user.id, instance.id)

    @classmethod
    def remove_member(cls, data, instance):
        user = UserService.get_user_by_email(data.get('email'))
        if user:
            cls._remove_user_team(user.profile, instance.id)
            user.profile.save()

    @classmethod
    def delete_team(cls, team):
        members = Profile.objects.filter(teams__contains=team.id)
        for member in members:
            cls._remove_user_team(member, team.id)
        members.bulk_update(members, ['teams'])

    @classmethod
    def get_leader(cls):
        users = User.objects.select_related('profile').values('id', 'email', 'profile__name').filter(active=1)
        return [{
            'id': user.get('id'),
            'email': user.get('email'),
            'name': user.get('profile__name')
        } for user in users]

    @classmethod
    def get_potential_members(cls, instance):
        profiles = Profile.objects.select_related('user').filter(user__active=1).exclude(
            teams__regex=r'(^|,)' + str(instance.id) + '(,|$)').values('name', 'user__email')
        return [{
            'name': profile.get('name'),
            'email': profile.get('user__email')
        } for profile in profiles]

    @classmethod
    def get_profile(cls, data, instance, leaders):
        check = True
        data.update(leader_name="No leader")
        if data.get("team_leader"):
            for leader in leaders:
                if cls.leader_accept(data, leader):
                    data.update(leader_name=leader.get("name", "No leader"))
                    check = False
                    break
        if check:
            data.update(team_leader=0)

        profiles = Profile.objects.filter(teams__regex=r'(^|,)' + str(instance.pk) + '(,|$)').select_related('user')
        for profile in profiles:
            profile.team_leader_id = data.get("team_leader")
        data.update(
            employee_number=profiles.count(),
            employee_list=TeamProfile(profiles, many=True).data,
            non_members=cls.get_potential_members(instance)
        )
        return data

    @classmethod
    def leader_accept(cls, data, leader):
        return data.get("team_leader") == leader.get('user_id') and leader.get('user__active') and leader.get('teams') \
               and str(data.get('id')) in leader.get('teams').split(',')

    @classmethod
    def update_user_team(cls, user_id, team_id):
        user = Profile.objects.get(user=user_id)
        if user.teams:
            user.teams = str(team_id) + "," + user.teams
        else:
            user.teams = str(team_id)
        user.save()

    @classmethod
    def _remove_user_team(cls, member, team_id):
        member.teams = (',' + member.teams + ',').replace(',' + str(team_id) + ',', ',')[1:-1]
        if member.teams == "":
            member.teams = None

    @classmethod
    def set_leader(cls, team, **kwargs):
        email = kwargs.get('email')
        user = UserService.get_user_by_email(email)
        if user:
            team.team_leader = user.id
            team.save()

    @classmethod
    def move_team(cls, user_id, current_team_id, new_team_id):
        user_profile = Profile.objects.get(id=user_id)
        cls._remove_user_team(user_profile, current_team_id)
        user_profile.save()
        cls.update_user_team(user_id, new_team_id)
