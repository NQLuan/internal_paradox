import json
from django.urls import reverse
from rest_framework import status
from api_user.models import User, Profile
from api_workday.models.type_off import TypeOff
import random
import uuid

from rest_framework.test import APITestCase

class TypeOffTesting(APITestCase):

    def setUp(self):
        self.uuid_cus = uuid.uuid1(random.randint(0, 2 ** 48 - 1))
        self.title = 'title'
        self.label = 'label'
        self.descriptions = 'descriptions'
        self.add_sub_day_off = 2
        self.email = 'email@gmail.com'
        self.password = 'foobar'
        self.authentication()
        self.type_off = TypeOff.objects.create(
            title=self.title,
            label=self.label,
            descriptions=self.descriptions
        )
        self.vaData = {
            "title": "Annual leave",
            "label": "Company paid",
            "descriptions": "No have"
        }

    def authentication(self):
        user = User(
            email=self.email,
            password=self.password,
            staff=True
        )
        user.save()
        user.set_password(user.password)
        user.save()
        Profile.objects.create(user=user, name="Test User")

        url = '/api/v1/login/'
        payload = {
            'email': user.email,
            'password': self.password
        }
        res = self.client.post(url, data=payload)
        response_data = json.loads(res.content)
        token = response_data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=token)
    #GET
    def test_get_type_off(self):
        self.client.credentials()
        url = reverse('type')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #CREATE
    def test_create_type_off_with_valid_input(self):
        url = reverse('create-type')
        response = self.client.post(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_type_off_without_credential(self):
        url = reverse('create-type')
        self.client.credentials()
        response = self.client.post(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_type_off_with_invalid_input(self):
        url = reverse('create-type')
        data = {
            "title": self.title,
            "label": self.label
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #EDIT
    def test_edit_type_off_with_out_credential(self):
        url = reverse('modify-type', args=[self.type_off.id])
        self.client.credentials()
        response = self.client.put(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_type_off(self):
        url = reverse('modify-type', args=[self.type_off.id])
        response = self.client.put(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_type_off(self):
        url = reverse('modify-type', args=[self.type_off.id])
        data = {
            "title": self.title,
            "label": self.label
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_type_off_with_invalid_id(self):
        url = reverse('modify-type', args=[self.uuid_cus])
        response = self.client.put(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #DELETE
    def test_delete_type_off_with_out_credential(self):
        url = reverse('modify-type', args=[self.type_off.id])
        self.client.credentials()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_type_off(self):
        url = reverse('modify-type', args=[self.type_off.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_type_off_with_invalid_id(self):
        url = reverse('modify-type', args=[self.uuid_cus])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)