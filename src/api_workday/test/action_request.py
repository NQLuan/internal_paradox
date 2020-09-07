import json
from django.urls import reverse
from rest_framework import status
from faker import Factory
from rest_framework.test import APITestCase

from .factories import TypeOffFactory
from .factories.user_authen import UserFactory, ProfileFactory, authentication
from .factories.company import CompanyFactory
from .factories.request_off import RequestOffFactory
from api_user.models import Profile
from api_workday.services.action_request import ActionRequestService
from api_workday.models import RequestDetail
from api_workday.constants import Workday

faker = Factory.create()
import datetime


class ActionRequestTesting(APITestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user1_profile = ProfileFactory.create(user=self.user1)

        self.user2 = UserFactory()
        self.user2_profile = ProfileFactory.create(user=self.user2, line_manager=self.user1_profile)

        self.user3 = UserFactory()
        self.user3_profile = ProfileFactory.create(user=self.user3, line_manager=self.user2_profile)

        self.user4 = UserFactory()
        self.user4_profile = ProfileFactory.create(user=self.user4, line_manager=self.user1_profile)

        self.company = CompanyFactory()

        self.type_off = TypeOffFactory()
        self.vaData = {
            "reason": faker.word(),
            "type_id": self.type_off.id,
            "date": [{"date": "2026-09-30", "type": "All day", "lunch": "False"},
                     {"date": "2025-09-30", "type": "Morning", "lunch": "True"}]
        }
        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user3))
        self.url_request = '/api/v1/workday/request/create'
        self.url_action = '/api/v1/workday/action'
        self.url_get_request = '/api/v1/workday/request/management'
        response_request = self.client.post(self.url_request, data=self.vaData)
        self.response_request_data = json.loads(response_request.content)
        self.action_approve_data = {
            'request_off_id': self.response_request_data['id'],
            'action': Workday.STATUS_APPROVED
        }

        self.action_reject_data = {
            'request_off_id': self.response_request_data['id'],
            'action': Workday.STATUS_REJECTED,
            'comment': ''
        }

        self.action_cancel_data = {
            'request_off_id': self.response_request_data['id'],
            'action': Workday.STATUS_CANCEL,
        }

    def test_action_approved_request_with_two_line_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user2))

        response_action = self.client.post(self.url_action, data=self.action_approve_data)
        response_action_data = json.loads(response_action.content)

        self.assertEqual(response_action_data['request_off_id']['status'], Workday.STATUS_FORWARDED)
        self.assertEqual(response_action_data['status'], Workday.STATUS_APPROVED)
        self.assertEqual(response_action.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user1))
        response_action = self.client.post(self.url_action, data=self.action_approve_data)
        response_action_data = json.loads(response_action.content)
        self.assertEqual(response_action_data['request_off_id']['status'], Workday.STATUS_APPROVED)
        self.assertEqual(response_action_data['status'], Workday.STATUS_APPROVED)
        self.assertEqual(response_action.status_code, status.HTTP_201_CREATED)

    def test_action_approved_request_with_one_line_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user4))

        data_request = {
            "reason": faker.word(),
            "type_id": self.type_off.id,
            "date": [{"date": "2026-08-30", "type": "All day", "lunch": "False"}]
        }

        response = self.client.post(self.url_request, data=data_request)
        response_data = json.loads(response.content)

        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user1))

        data = {
            'request_off_id': response_data['id'],
            'action': Workday.STATUS_APPROVED
        }

        response_action = self.client.post(self.url_action, data=data)
        response_action_data = json.loads(response_action.content)

        self.assertEqual(response_action_data['request_off_id']['status'], Workday.STATUS_APPROVED)
        self.assertEqual(response_action_data['status'], Workday.STATUS_APPROVED)
        self.assertEqual(response_action.status_code, status.HTTP_201_CREATED)

    def test_first_user_action_rejected_request_with_two_line_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user2))
        response_action = self.client.post(self.url_action, data=self.action_reject_data)
        response_action_data = json.loads(response_action.content)
        self.assertEqual(response_action_data['request_off_id']['status'], Workday.STATUS_REJECTED)
        self.assertEqual(response_action_data['status'], Workday.STATUS_REJECTED)
        self.assertEqual(response_action.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user1))

        response_action = self.client.post(self.url_action, data=self.action_reject_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

        response_action = self.client.post(self.url_action, data=self.action_approve_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

    def test_second_user_action_rejected_request_with_two_line_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user2))

        response_action = self.client.post(self.url_action, data=self.action_approve_data)
        response_action_data = json.loads(response_action.content)

        self.assertEqual(response_action_data['request_off_id']['status'], Workday.STATUS_FORWARDED)
        self.assertEqual(response_action_data['status'], Workday.STATUS_APPROVED)
        self.assertEqual(response_action.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user1))

        response_action = self.client.post(self.url_action, data=self.action_reject_data)
        response_action_data = json.loads(response_action.content)

        self.assertEqual(response_action_data['request_off_id']['status'], Workday.STATUS_REJECTED)
        self.assertEqual(response_action_data['status'], Workday.STATUS_REJECTED)
        self.assertEqual(response_action.status_code, status.HTTP_201_CREATED)

    def test_action_cancel_request_with_request_of_user(self):

        response_action = self.client.post(self.url_action, self.action_cancel_data)
        response_action_data = json.loads(response_action.content)
        self.assertEqual(response_action_data['status'], Workday.STATUS_CANCEL)
        self.assertEqual(response_action.status_code, status.HTTP_201_CREATED)

    def test_action_request_with_user_no_line_manger(self):
        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user4))

        response_action = self.client.post(self.url_action, self.action_approve_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

        response_action = self.client.post(self.url_action, self.action_reject_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

        response_action = self.client.post(self.url_action, self.action_cancel_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

    def test_action_approved_or_rejected_request_by_user(self):
        response_action = self.client.post(self.url_action, data=self.action_approve_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

        response_action = self.client.post(self.url_action, data=self.action_reject_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

    def test_action_approved_request_with_request_canceled(self):
        self.client.post(self.url_action, self.action_cancel_data)

        response_action = self.client.post(self.url_action, self.action_approve_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

    def test_action_rejected_request_with_request_canceled(self):
        self.client.post((self.url_action, self.action_cancel_data))

        response_action = self.client.post(self.url_action, self.action_reject_data)
        self.assertEqual(response_action.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request_off_by_user_line_manager(self):
        RequestOffFactory.create(profile=self.user2_profile)

        self.client.credentials(HTTP_AUTHORIZATION=authentication(self.user2))

        response = self.client.get(self.url_get_request)
        print(response.content)
