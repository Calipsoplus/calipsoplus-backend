from django.contrib.auth.models import User

import logging


from rest_framework import status
from rest_framework.utils import json

from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class UserViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):

        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.test_user = User.objects.create_user(**self.credentials)

    def test_login_user_200(self):
        self.logger.debug('#### test_login_user_200')

        url = '/login/'
        data_str = json.dumps(self.credentials)
        response = self.client.post(url, format='json', content_type='application/json', data=data_str)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_401(self):
        self.logger.debug('#### test_login_user_401')

        self.credentials = {
            'username': 'testuser',
            'password': 'surprise'}

        url = '/login/'
        data_str = json.dumps(self.credentials)
        response = self.client.post(url, format='json', content_type='application/json', data=data_str)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_credentials_no_pass_400(self):
        self.logger.debug('#### test_login_invalid_credentials_no_pass_400')

        self.credentials = {'username': 'testuser'}

        url = '/login/'
        data_str = json.dumps(self.credentials)
        response = self.client.post(url, format='json', content_type='application/json', data=data_str)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_credentials_no_username_400(self):
        self.logger.debug('#### test_login_invalid_credentials_no_username_400')

        self.credentials = {'password': 'secret'}

        url = '/login/'
        data_str = json.dumps(self.credentials)
        response = self.client.post(url, format='json', content_type='application/json', data=data_str)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_credentials_400(self):
        self.logger.debug('#### test_login_invalid_credentials_400')

        self.credentials = ''

        url = '/login/'
        data_str = json.dumps(self.credentials)
        response = self.client.post(url, format='json', content_type='application/json', data=data_str)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

