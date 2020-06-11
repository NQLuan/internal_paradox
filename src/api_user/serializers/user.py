from rest_framework import serializers

from api_user.models import User
from api_user.serializers import ProfileSerializers


class UserSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializers(many=True, required=True)

    # TODO Work on this until UI changes
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user_profile = ret.get("user_profile")[0]
        ret.update(
            name=user_profile.get('name'),
            phone=user_profile.get('phone'),
            teams=user_profile.get('teams'),
            personal_email=user_profile.get('personal_email'),
            identity_number=user_profile.get('identity_number'),
            birth_day=user_profile.get('birth_day'),
            account_number=user_profile.get('account_number'),
            bank=user_profile.get('bank'),
            image=user_profile.get('image'),
            team_name=user_profile.get('team_name')
        )
        return ret

    class Meta:
        model = User
        fields = ('id', 'email', 'profile', 'user_profile', 'active')
