from rest_framework import serializers

from api.models import Profile


class ProfileSerializers(serializers.ModelSerializer):
    active = serializers.CharField(source="user.active", required=False)

    class Meta:
        model = Profile
        fields = ('id', 'name', 'phone', 'personal_email', 'identity_number', 'teams',
                  'birth_day', 'account_number', 'join_date', 'bank', 'active', 'join_date', 'image')


class ProfileName(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name')


class ProfileLunch(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'lunch', 'lunch_weekly', 'veggie')
