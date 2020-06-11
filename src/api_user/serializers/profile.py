from rest_framework import serializers

from api_base.services import Utils
from api_team.models import Team
from api_user.models import Profile
from api_user.serializers import PhotoSerializer


class ProfileSerializers(serializers.ModelSerializer):
    photo = PhotoSerializer(many=True, required=False)
    active = serializers.CharField(source="user.active", required=False)

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)

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


class ProfileName(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name')


class ProfileLunch(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'lunch', 'lunch_weekly', 'veggie')
