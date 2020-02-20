from rest_framework import serializers

from api.models import Team


class TeamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'team_name', 'team_email', 'team_leader')
