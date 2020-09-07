from api_user.models import User, Profile
import factory
from faker import Factory
import json

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email', 'staff')

    email = faker.email()
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    staff = True


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile


def authentication(self):
    user = UserFactory()
    url = '/api/v1/login/'
    profile = ProfileFactory(user=user, name='Test')
    payload = {
        'email': user.email,
        'password': 'defaultpassword'
    }
    res = self.client.post(url, data=payload)
    response_data = json.loads(res.content)
    token = response_data.get('token')
    return token, profile
