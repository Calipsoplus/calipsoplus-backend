from rest_framework.test import APITestCase

import logging

from apprest.models.experiment import CalipsoExperiment
from apprest.models.user import CalipsoUser
from apprest.services.experiment import CalipsoExperimentsServices

logger = logging.getLogger(__name__)


class ExperimentServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['users.json', 'experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp ExperimentServiceTestCase START ####')

        self.calipso_user = CalipsoUser.objects.get(pk=1)
        self.experiment_1 = CalipsoExperiment.objects.get(pk=1)
        self.experiment_2 = CalipsoExperiment.objects.get(pk=2)

        self.calipso_user.experiments.add(self.experiment1)
        self.calipso_user.experiments.add(self.experiment2)

        self.service = CalipsoExperimentsServices()

        logger.debug('#### setUp ExperimentServiceTestCase END ####')

    def test_service_experiments(self):
        self.logger.debug('#### TEST test_service_experiments START ####')
        all_experiments = self.service.get_user_experiments(self.user.username)
        self.assertEqual(len(all_experiments), 2)
        self.logger.debug('#### TEST test_service_experiments END ####')