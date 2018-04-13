from rest_framework.test import APITestCase
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




