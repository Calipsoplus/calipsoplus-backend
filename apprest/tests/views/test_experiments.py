import json
from rest_framework import status

import logging

from apprest.models.experiment import CalipsoExperiment
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
        self.experiment_2 = CalipsoExperiment.objects.create(subject='Experiment 2', body='Experiment to look at ...')

        self.logger.debug('#### setUp END ####')

