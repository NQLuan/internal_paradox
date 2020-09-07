import json
from django.urls import reverse
from rest_framework import status
import random
import uuid
from api_workday.tests.factories import TypeOffFactory
from api_workday.models.type_off import TypeOff
from api_workday.utils.user_auth import authentication
from faker import Factory
from rest_framework.test import APITestCase

faker = Factory.create()

class TypeOffTesting(APITestCase):

    def setUp(self):
        self.uuid_cus = uuid.uuid1(random.randint(0, 2 ** 48 - 1))
        self.client.credentials(HTTP_AUTHORIZATION=authentication(self)[0])
        self.type_off = TypeOffFactory()
        self.lenTypeOff = TypeOff.objects.count()
        self.vaData = {
            "title": faker.word(),
            "label": faker.word(),
            "descriptions": faker.text()
        }

    #GET
    def test_get_type_off(self):
        self.client.credentials()
        url = reverse('type')
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content)[0]['id'], str(self.type_off.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #CREATE
    def test_create_type_off_with_valid_input(self):
        url = reverse('create-type')
        response = self.client.post(url, data=self.vaData)
        data = json.loads(response.content)
        create_data = {
            "title": data["title"],
            "label": data["label"],
            "descriptions": data["descriptions"]
        }
        self.assertEqual(create_data, self.vaData)
        self.assertEqual(TypeOff.objects.count() - self.lenTypeOff, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_type_off_without_credential(self):
        url = reverse('create-type')
        self.client.credentials()
        response = self.client.post(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_type_off_with_invalid_input(self):
        url = reverse('create-type')
        data = {
            "title": faker.word(),
            "label": faker.word()
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #EDIT
    def test_edit_type_off_with_out_credential(self):
        url = reverse('modify-type', args=[self.type_off.id])
        self.client.credentials()
        response = self.client.put(url, data=self.vaData)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_type_off_with_valid_input(self):
        url = reverse('modify-type', args=[self.type_off.id])
        response = self.client.put(url, data=self.vaData)
        data = json.loads(response.content)
        create_data = {
            "title": data["title"],
            "label": data["label"],
            "descriptions": data["descriptions"]
        }
        self.assertEqual(create_data, self.vaData)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_type_off_with_invalid_input(self):
        url = reverse('modify-type', args=[self.type_off.id])
        data = {
            "title": faker.word(),
            "label": faker.word()
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
        self.assertEqual(TypeOff.objects.count() - self.lenTypeOff, -1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_type_off_with_invalid_id(self):
        url = reverse('modify-type', args=[self.uuid_cus])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
