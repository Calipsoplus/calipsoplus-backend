import logging
from rest_framework import status

from apprest.models.user import CalipsoUser
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ExperimentViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.scientist_1 = CalipsoUser.objects.get(pk=1)
        self.scientist_2 = CalipsoUser.objects.get(pk=2)
        self.scientist_3 = CalipsoUser.objects.get(pk=3)
        self.scientist_4 = CalipsoUser.objects.get(pk=4)

        self.logger.debug('#### setUp END ####')

    def test_get_experiments_by_username(self):
        self.logger.debug('#### TEST get experiments by username START ####')

        base_url = '/users/%s/experiments/'

        # Not authenticated -> 403
        url = base_url % self.scientist_1.user.username
        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Login and check methods
        self.login_and_check_http_methods(self.scientist_1.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        # No user specified -> 404
        url = base_url % ''
        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test with non-existing user -> 404
        url = base_url % 'xxxxx'
        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test with valid user -> 200
        url = base_url % self.scientist_1.user.username
        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # TODO: Test response structure
        self.logger.debug('#### TEST get experiments by login END ####')
