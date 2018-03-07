from rest_framework.test import APITestCase

import logging

from apprest.models.experiments import CalipsoExperiment
from apprest.services.experiment import CalipsoExperimentsServices

logger = logging.getLogger(__name__)


class ExperimentServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.service = CalipsoExperimentsServices()
        self.experiments = ['EXP1', 'EXP2', 'EXP3']

        self.logger.debug('#### setUp END ####')

    def test_get_all_experiments(self):
        self.logger.debug('#### TEST get_all_experiments START ####')

        # create experiments
        for experiment in self.experiments:
            CalipsoExperiment.objects.create(subject=experiment, body='experiment for test')

        # get_all_experiments
        all_experiments = self.service.get_all_experiments()
        self.assertEqual(len(all_experiments), len(self.experiments) + 2) # two from fixtures

        self.logger.debug('#### TEST get_all_experiments END ####')

    def test_get_one_experiments(self):
        self.logger.debug('#### TEST get_one_experiment START ####')

        # get one experiments
        one_experiment = self.service.get_experiment(1)
        self.assertEqual(one_experiment.subject,'Experiment 1')

        self.logger.debug('#### TEST get_all_experiments END ####')

