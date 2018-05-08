import json

from django.contrib.auth.models import User
from rest_framework import status

import logging

from apprest.models.experiment import CalipsoExperiment
from apprest.models.user import CalipsoUser
from apprest.services.experiment import CalipsoExperimentsServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class UserExperimentViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    # fixtures = ['experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.service = CalipsoExperimentsServices()

        self.user_alex = User.objects.create_user(username='acampsm')

        self.experiment_1 = CalipsoExperiment(subject='Experiment 1', body='Experiment 2 to look at ...')
        self.experiment_2 = CalipsoExperiment(subject='Experiment 2', body='Experiment 2 to look at ...')
        self.experiment_1.save()
        self.experiment_2.save()

        self.calipso_user = CalipsoUser.objects.get(user=self.user_alex)

        self.calipso_user.experiments.add(self.experiment_1)
        self.calipso_user.experiments.add(self.experiment_2)

        self.logger.debug('#### setUp END ####')

    def test_get_user_experiments(self):
        self.logger.debug('#### TEST test_get_user_experiments START ####')
        url = '/user/' + str(self.user_alex.username) + '/experiment/'

        # Should return status 200 if everything goes fine
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug('# response.content --> %s' % response.content)

        json_content = json.loads(response.content.decode("utf-8"))
        self.logger.debug('# RESPONSE --> %s' % json_content)
        self.assertIsInstance(json_content, list)
        self.assertGreater(len(json_content), 0)

        self.logger.debug('#### TEST get test_get_user_experiments by pk END ####')
