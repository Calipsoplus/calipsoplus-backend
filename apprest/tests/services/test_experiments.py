from django.contrib.auth.models import User
from rest_framework.test import APITestCase

import logging

from apprest.models.user import CalipsoUser
from apprest.services.experiment import CalipsoExperimentsServices

logger = logging.getLogger(__name__)


class ExperimentServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp ExperimentServiceTestCase START ####')

        self.user = User.objects.create_user(username='acampsm', password='1234')
        self.calipso_user = CalipsoUser.objects.get(user=self.user)

        self.experiments = ['EXP1', 'EXP2', 'EXP3']

        self.calipso_user.add(self.experiments)

        self.service = CalipsoExperimentsServices()

        self.logger.debug('#### setUp ExperimentServiceTestCase END ####')


    def test_service_experiments(self):
        self.logger.debug('#### TEST test_service_experiments END ####')
        all_experiments = self.service.get_user_experiments(self.calipso_user.id)
        self.assertEqual(len(all_experiments), len(self.experiments))
        self.logger.debug('#### TEST test_service_experiments END ####')
