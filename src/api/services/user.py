#!/usr/bin/env python

# author Huy
# date 7/30/2019
from django.conf import settings

from api.models import Photo, Team
from api.serializers import PhotoSerializer
from api.services import BaseService


class UserService(BaseService):

    @staticmethod
    def get_team(users):
        for user in users:
            teams = []
            if user['teams'] is not None:
                for j in user['teams'].split(','):
                    teams.append({'id': j,
                                  'name': Team.objects.get(id=int(j)).team_name})
            else:
                teams.append("No team")
                user['teams'] = "9999"
            user['team_name'] = teams
        return users

    @staticmethod
    def get_photo(data):
        data = UserService.get_team([data])[0]
        photos = Photo.objects.filter(profile_id=data.get('profile'))
        serializer = PhotoSerializer(photos, many=True)
        for i in serializer.data:
            i['photo'] = f'http://{settings.IP[0]}:{settings.API_PORT}{i.get("photo")}'
        data['photos'] = serializer.data
        return data

    @staticmethod
    def convert_to_int(string):
        try:
            number = int(string)
        except ValueError:
            number = 0
        return number
