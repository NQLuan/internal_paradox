from django.urls import reverse
from rest_framework.test import APITestCase, URLPatternsTestCase, force_authenticate
from django.urls import include, path, reverse

from rest_framework import status
from api_user.models import User
from api_user.views import profile
from api_user.models.profile import Profile
import json


class ProfileTests(APITestCase):
    
    def setUp(self):        
        self.password = '123456'
        self.super_user = User.objects.create_user(email='admin@gmail.com', password=self.password, is_admin=1, is_staff=1)
        self.super_user_profile = Profile.objects.create(user=self.super_user)
        self.normal_user = User.objects.create_user('user@gmail.com', self.password)
        self.normal_user_profile = Profile.objects.create(user=self.normal_user)
        self.assigned_manager = User.objects.create_user('manager@gmail.com', self.password)
        self.assigned_manager_profile = Profile.objects.create(user=self.assigned_manager)

    def authentication(self, user):
        url = '/api/v1/login/'
        payload = {
            'email': user.email,
            'password': self.password
        }
        res = self.client.post(url, data=payload)
        response_data = json.loads(res.content)
        token = response_data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=token)


    def test_admin_set_line_manager(self):
        url = reverse('profile-set-line-manager', kwargs={ 'pk': self.normal_user_profile.id })
        data = { 'profile_id': f'{self.assigned_manager_profile.id}' }
        self.authentication(self.super_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_set_line_manager_not_exist(self):
        url = reverse('profile-set-line-manager', kwargs={ 'pk': self.normal_user_profile.id })
        data = { 'profile_id': 12 }
        self.authentication(self.super_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_admin_set_line_manager(self):
        url = reverse('profile-set-line-manager', kwargs={ 'pk': self.normal_user_profile.id })
        data = { 'profile_id': f'{self.assigned_manager_profile.id}' }
        self.authentication(self.normal_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

