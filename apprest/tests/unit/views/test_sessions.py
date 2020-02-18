import logging
from rest_framework import status

from apprest.models.user import CalipsoUser
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class SessionViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'experiments.json', 'sessions.json', 'users_experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.scientist_1 = CalipsoUser.objects.get(pk=1)
        self.logger.debug('#### setUp END ####')

    def test_get_json_sessions_from_experiment(self):
        self.logger.debug('#### TEST test_get_json_sessions_from_experiment START ####')

        base_url = '/users/%s/experiments/'
        url = base_url % self.scientist_1.user.username

        # Login and check methods
        self.login_and_check_http_methods(self.scientist_1.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        response = self.client.get(url, format='json', content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_content = response.json()

        self.assertEqual(len(json_content['results']), 2)
        self.logger.debug('#### TEST test_get_json_sessions_from_experiment END ####')
