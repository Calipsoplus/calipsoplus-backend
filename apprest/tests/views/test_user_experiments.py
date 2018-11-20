import json
import logging

from rest_framework import status

from apprest.models.user import CalipsoUser
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class UserExperimentViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['users.json', 'experiments.json', 'users_experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.logger.debug('#### setUp END ####')

    def test_get_two_user_experiments(self):
        self.logger.debug('#### TEST test_get_two_user_experiments START ####')

        calipso_user = CalipsoUser.objects.get(pk=1)
        base_url = '/experiments/%s/'
        url = base_url % str(calipso_user.user.username)

        # Login and check methods
        self.login_and_check_http_methods(calipso_user.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        # Should return status 200 if everything goes fine
        response = self.client.get(url, format='json', content_type='application/json')

        json_content = json.loads(response.content.decode("utf-8"))
        self.logger.debug('# RESPONSE --> %s' % json_content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(json_content), 0)
        self.assertEqual(json_content['count'], 2) # two

        self.logger.debug('#### TEST get test_get_two_user_experiments END ####')

    def test_get_one_user_experiments(self):
        self.logger.debug('#### TEST test_get_one_user_experiments START ####')
        calipso_user = CalipsoUser.objects.get(pk=2)
        base_url = '/experiments/%s/'
        url = base_url % str(calipso_user.user.username)

        # Login and check methods
        self.login_and_check_http_methods(calipso_user.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        # Should return status 200 if everything goes fine
        response = self.client.get(url, format='json', content_type='application/json')

        json_content = json.loads(response.content.decode("utf-8"))
        self.logger.debug('# RESPONSE --> %s' % json_content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(json_content), 0)
        self.assertEqual(json_content['count'], 1) # only one

        self.logger.debug('#### TEST get test_get_one_user_experiments by pk END ####')
