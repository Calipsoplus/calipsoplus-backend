from rest_framework.test import APITestCase


from django.contrib.auth.models import User

import logging

from apprest.services.user import CalipsoUserServices

logger = logging.getLogger(__name__)


class UserServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.service = CalipsoUserServices()
        self.users = ['acampsm', 'dsanchez', 'anfernandez']

        self.logger.debug('#### setUp END ####')

    def test_get_all_users(self):
        self.logger.debug('#### TEST get_all_users START ####')

        # create users
        for user in self.users:
            User.objects.create_user(username=user, password='1234')

        # get_all_users
        all_users = self.service.get_all_users()
        self.assertEqual(len(all_users), len(self.users))  # misuser already created

        self.logger.debug('#### TEST get_all_users END ####')
