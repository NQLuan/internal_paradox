from django.urls import reverse
import json
from rest_framework import status
from api_workday.utils.user_auth import authentication
import random
import uuid
from rest_framework.test import APITestCase
from api_workday.test.factories.request_off import RequestOffFactory
from api_workday.test.factories import TypeOffFactory
from faker import Factory
from api_workday.models.request_off import RequestOff

faker = Factory.create()

class RequestOfTesting(APITestCase):
    def setUp(self):
        self.uuid_cus = uuid.uuid1(random.randint(0, 2 ** 48 - 1))
        self.data = authentication(self)
        self.client.credentials(HTTP_AUTHORIZATION=self.data[0])
        self.request_off = RequestOffFactory(profile=self.data[1])
        self.lenRequestOff = RequestOff.objects.count()
        self.type_off = TypeOffFactory()
        self.vaData = {
            "reason": faker.word(),
            "type_id": self.type_off.id,
            "date":  [{"date": "2026-09-30", "type": "All day", "lunch": "False"},
                      {"date": "2025-09-30", "type": "Morning", "lunch": "True"}]
        }

    #GET
    def test_get_request_off(self):
        url = reverse('request-detail', args=[self.request_off.id])
        request_off = RequestOff.objects.get(pk=self.request_off.id)
        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], str(request_off.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_off_with_out_credential(self):
        url = reverse('request-detail', args=[self.request_off.id])
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # CREATE
    def test_create_request_off_with_valid_input(self):
        url = reverse('create-request')
        response = self.client.post(url, data=self.vaData)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['reason'], self.vaData['reason'])
        self.assertEqual(RequestOff.objects.count() - self.lenRequestOff, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_request_off_without_credential(self):
        url = reverse('create-request')
        self.client.credentials()
        response = self.client.post(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_request_off_with_invalid_input(self):
        url = reverse('create-request')
        data = {
            "reason": '',
            "date": [{"date": "2026-09-30", "type": "All day", "lunch": "False"},
                     {"date": "2025-09-30", "type": "Morning", "lunch": "True"}]
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #EDIT
    def test_edit_request_off_with_out_credential(self):
        url = reverse('request-detail', args=[self.request_off.id])
        self.client.credentials()
        response = self.client.put(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_request_off(self):
        url = reverse('request-detail', args=[self.request_off.id])
        request_off = RequestOff.objects.get(pk=self.request_off.id)
        response = self.client.put(url, data=self.vaData)
        response_data = json.loads(response.content)
        self.assertNotEqual(response_data['reason'], request_off.reason)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_request_off_with_invalid_id(self):
        url = reverse('request-detail', args=[self.uuid_cus])
        response = self.client.put(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #DELETE
    def test_delete_request_off_with_out_credential(self):
        url = reverse('request-detail', args=[self.request_off.id])
        self.client.credentials()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_request_off(self):
        url = reverse('request-detail', args=[self.request_off.id])
        response = self.client.delete(url)
        self.assertEqual(RequestOff.objects.count() - self.lenRequestOff, -1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_request_off_with_invalid_id(self):
        url = reverse('request-detail', args=[self.uuid_cus])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
