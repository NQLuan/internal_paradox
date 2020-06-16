from rest_framework import serializers

from api_team.models import Team


class TeamSerializers(serializers.ModelSerializer):

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return super().to_representation(instance)

    class Meta:
        model = Team
        fields = ('id', 'team_name', 'team_email', 'team_leader')


class MemberSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField(max_length=255)
