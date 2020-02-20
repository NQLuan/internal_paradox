#!/usr/bin/env python

# author OS
# date 7/25/2019
from api.models import Profile, User
from api.services import BaseService, TeamUtil


class TeamService(BaseService):
    """
    LIST TEAM METHOD
    """

    @staticmethod
    def list_team_member(serializer_data):
        leaders = Profile.objects.select_related('user').values('user_id', 'user__active', 'teams', 'name')
        return [TeamUtil.get_profile(i, i['id'], leaders) for i in serializer_data]

    """
    RETRIEVE TEAM METHOD
    """

    @staticmethod
    def retrieve_team_member(serializer_data, instance):
        leaders = Profile.objects.select_related('user').filter(user_id=instance.team_leader).values(
            'user_id', 'user__active', 'teams', 'name')
        return {
            "team": TeamUtil.get_profile(serializer_data, instance.id, leaders)
        }

    """
    UPDATE TEAMS FIELD FOR MEMBERS
    """

    @staticmethod
    def add_new_member(data, instance):
        user = User.objects.get(email=data['email'])
        TeamUtil.update_teams(user.id, instance.id)

    @staticmethod
    def update_leader_teams(data):
        leader_id = data['team_leader']
        team_id = data['id']
        TeamUtil.update_teams(leader_id, team_id)

    """
    REMOVE TEAMS FIELD FOR MEMBERS
    """

    @staticmethod
    def remove_member(data, instance):
        user = User.objects.get(email=data['email'])
        TeamUtil.remove_team(user.profile, instance.id)
        user.profile.save()

    @staticmethod
    def remove_team(team):
        members = Profile.objects.filter(teams__contains=team.id)
        for member in members:
            TeamUtil.remove_team(member, team.id)
        members.bulk_update(members, ['teams'])

    """
    GET USER THAT IS NOT A LEADER
    """

    @staticmethod
    def get_leader():
        users = User.objects.select_related('profile').values('id', 'email', 'profile__name').filter(active=1)
        return [{
            'id': user['id'],
            'email': user['email'],
            'name': user['profile__name']
        } for user in users]

    """
    GET USER THAT IS NOT IN SPECIFIC TEAM
    """

    @staticmethod
    def get_potential_members(instance):
        profiles = Profile.objects.select_related('user').filter(user__active=1).exclude(
            teams__regex=r'(^|,)' + str(instance.id) + '(,|$)').values('name', 'user__email')
        return [{
            'name': profile['name'],
            'email': profile['user__email']
        } for profile in profiles]
