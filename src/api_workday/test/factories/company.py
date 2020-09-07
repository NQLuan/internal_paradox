from api_user.models import User, Profile
import factory
from faker import Factory
import json
from rest_framework.test import APIClient
from api_company.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
