import json
from django.urls import reverse
from rest_framework import status
from api_user.models import User, Profile
from api_workday.models.request_off import RequestOff
import random
import uuid

from rest_framework.test import APITestCase

class RequestOfTesting(APITestCase):
    def setUp(self):
        self.name = 'Do'