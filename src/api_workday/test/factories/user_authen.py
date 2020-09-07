from api_user.models import User, Profile
import factory
from faker import Factory
import json
from rest_framework.test import APIClient
from api_company.models import Company

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email', 'staff')

    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', '123456')
    staff = False


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile


def authentication(user):
    client = APIClient()
    url = '/api/v1/login/'
    payload = {
        'email': user.email,
        'password': '123456'
    }
    res = client.post(url, data=payload)
    response_data = json.loads(res.content)
    token = response_data.get('token')
    return token

