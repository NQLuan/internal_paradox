from django.conf import settings
from rest_framework import serializers

from api_base.services import Utils
from api_team.models import Team
from api_user.models import Profile
from api_user.serializers import PhotoSerializer
from api_workday.models import Lunch


class ProfileSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    photo = PhotoSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.update(active=instance.user.active)

        # Get team for each user
        teams = []
        team_ids = ret.get('teams', None)
        if team_ids:
            for team_id in ret.get('teams').split(','):
                teams.append({
                    'id': team_id,
                    'name': Team.objects.get(id=Utils.convert_to_int(team_id)).team_name
                })
        else:
            teams.append("No team")
            ret.update(teams=0)
        ret.update(team_name=teams)
        return ret

    def update(self, instance, validated_data):
        profile = super().update(instance, validated_data)
        email = validated_data.get('email')
        if email:
            profile.user.email = email
            profile.user.save()
        return profile


class ProfileName(serializers.ModelSerializer):
    day = serializers.DateField(required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        lunch_day = ret.get('day')
        lunch_objs = Lunch.objects.filter(date__date=lunch_day)
        lunch_profile_ids = list(lunch.profile_id for lunch in lunch_objs)
        if ret.get('id') in lunch_profile_ids:
            try:
                _lunch = lunch_objs.get(profile_id=ret.get('id'))
                ret.update(
                    lunch_id=_lunch.id,
                    status='Lunch'
                )
            except Lunch.DoesNotExist:
                ret.update(status='No lunch')
        else:
            ret.update(status='No lunch')
        return ret

    class Meta:
        model = Profile
        fields = ('id', 'name', 'day')


class ProfileLunch(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'lunch', 'lunch_weekly', 'veggie')


class TeamProfile(serializers.ModelSerializer):
    team_leader_id = serializers.IntegerField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('image'):
            ret.update(image=settings.MEDIA_IMAGE + ret.get('image'))
        role = "Leader" if ret.get('id') == instance.team_leader_id else "Member"
        ret.update(
            role=role,
            email=instance.user.email
        )
        return ret
