from django.contrib.auth.models import User
from rest_framework.test import APITestCase

import logging

from apprest.models.experiment import CalipsoExperiment
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

        experiment1 = CalipsoExperiment.objects.create(subject="SUBJECT1", body="BODY1")
        experiment2 = CalipsoExperiment.objects.create(subject="SUBJECT2", body="BODY2")

        self.calipso_user.experiments.add(experiment1)

        self.calipso_user.experiments.add(experiment2)

        self.service = CalipsoExperimentsServices()

        logger.debug('#### setUp ExperimentServiceTestCase END ####')

    def test_service_experiments(self):
        self.logger.debug('#### TEST test_service_experiments START ####')
        all_experiments = self.service.get_user_experiments(self.user.username)
        self.assertEqual(len(all_experiments), 2)
        self.logger.debug('#### TEST test_service_experiments END ####')