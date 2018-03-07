import json
from rest_framework import status

import logging

from apprest.models.experiments import CalipsoExperiment
from apprest.services.experiment import CalipsoExperimentsServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ExperimentViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.service = CalipsoExperimentsServices()
        self.experiment_1 = CalipsoExperiment.objects.create(subject='Experiment 1', body='Experiment to look at ...')

        self.logger.debug('#### setUp END ####')

    def test_get_all_experiments(self):
        self.logger.debug('#### TEST test_get_all_experiments START ####')

        url = '/experiments/all/'

        # Should return status 200 if everything goes fine

        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug('# response.content --> %s' % response.content)

        json_content = json.loads(response.content.decode("utf-8"))
        self.logger.debug('# RESPONSE --> %s' % json_content)
        self.assertIsInstance(json_content, list)
        self.assertGreater(len(json_content), 0)

        self.logger.debug('#### TEST get test_get_all_experiments by pk END ####')

    def test_get_experiment(self):
        self.logger.debug('#### TEST test_get_experiment START ####')

        url = '/experiments/1/'

        # Should return status 200 if everything goes fine

        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug('# response.content --> %s' % response.content)

        json_content = json.loads(response.content.decode("utf-8"))
        self.logger.debug('# RESPONSE --> %s' % json_content)

        self.assertIsInstance(json_content, dict)
        self.assertGreater(len(json_content), 0)

        self.logger.debug('#### TEST get test_get_experiment END ####')

