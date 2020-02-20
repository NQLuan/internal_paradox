from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="profile.name", required=False)
    phone = serializers.CharField(source="profile.phone", required=False)
    personal_email = serializers.EmailField(source="profile.personal_email", required=False)
    identity_number = serializers.CharField(source="profile.identity_number", required=False)
    birth_day = serializers.DateField(source="profile.birth_day", required=False)
    teams = serializers.CharField(source="profile.teams", required=False)
    account_number = serializers.CharField(source="profile.account_number", required=False)
    bank = serializers.CharField(source="profile.bank", required=False)
    image = serializers.ImageField(source="profile.image", required=False)

    class Meta:
        model = User
        fields = ('id', 'profile', 'name', 'phone', 'email', 'teams',
                  'personal_email', 'identity_number', 'birth_day',
                  'account_number', 'bank', 'active', 'image')


class MemberSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField(max_length=255)
