import json
import logging

from rest_framework import status

from apprest.models.experiment import CalipsoExperiment, CalipsoUserExperiment
from apprest.models.user import CalipsoUser
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class UserExperimentViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['users.json', 'experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.calipso_user = CalipsoUser.objects.get(pk=1)

        self.experiment_1 = CalipsoExperiment.objects.get(pk=1)
        self.experiment_2 = CalipsoExperiment.objects.get(pk=2)

        calipso_user_experiment = CalipsoUserExperiment(calipso_user=self.calipso_user,
                                                        calipso_experiment=self.experiment_1)
        calipso_user_experiment.save()

        calipso_user_experiment = CalipsoUserExperiment(calipso_user=self.calipso_user,
                                                        calipso_experiment=self.experiment_2)
        calipso_user_experiment.save()

        self.logger.debug('#### setUp END ####')

    def test_get_user_experiments(self):
        self.logger.debug('#### TEST test_get_user_experiments START ####')
        base_url = '/experiments/%s/'
        url = base_url % str(self.calipso_user.user.username)

        # Login and check methods
        self.login_and_check_http_methods(self.calipso_user.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        # Should return status 200 if everything goes fine
        response = self.client.get(url, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_content = json.loads(response.content.decode("utf-8"))

        self.assertGreater(len(json_content), 0)

        self.logger.debug('#### TEST get test_get_user_experiments by pk END ####')