import json
from rest_framework import status
from django.contrib.auth.models import User

import logging

from apprest.models.user import CalipsoUser
from apprest.services.user import CalipsoUserServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class UserViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.service = CalipsoUserServices()
        self.user_alex = User.objects.create_user(username='acampsm')
        self.user_alex_id = self.user_alex.id
        self.unauthorized_user = User.objects.create_user(username='unauthorized')

        self.logger.debug('#### setUp END ####')

    def test_get_all_users(self):
        self.logger.debug('#### TEST get_all_users START ####')

        url = '/users/all/'

        self.login_and_check_http_methods('acampsm', url, ['GET'])

        # Should return status 200 if everything goes fine

        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug('# response.content --> %s' % response.content)

        json_content = json.loads(response.content.decode("utf-8"))
        self.logger.debug('# RESPONSE --> %s' % json_content)
        self.assertIsInstance(json_content, list)
        self.assertGreater(len(json_content), 0)

        self.logger.debug('#### TEST get time_entry by pk END ####')


    def test_get_a_user(self):
        self.logger.debug('#### TEST test_get_a_user START ####')

        url = '/users/'+str(self.user_alex_id)+'/'

        self.login_and_check_http_methods('acampsm', url, ['GET'])

        # Should return status 200 if everything goes fine

        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug('# response.content --> %s' % response.content)

        json_content = json.loads(response.content.decode("utf-8"))
        self.logger.debug('# RESPONSE --> %s' % json_content)
        self.assertIsInstance(json_content, dict)
        self.assertGreater(len(json_content), 0)

        self.logger.debug('#### TEST get test_get_a_user by pk END ####')
