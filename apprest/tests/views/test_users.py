from django.contrib.auth.models import User

import logging

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

