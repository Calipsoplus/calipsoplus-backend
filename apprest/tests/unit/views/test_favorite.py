import logging

from rest_framework import status
from rest_framework.utils import json

from apprest.models.user import CalipsoUser
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class FavoriteExperimentViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'experiments.json', 'users_experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.calipso_user = CalipsoUser.objects.get(pk=1)
        self.logger.debug('#### setUp END ####')

    def test_set_favorite(self):
        url = '/favorite/2/'

        data = {"calipso_user": 1, "calipso_experiment": 2, "favorite": 1}
        data_str = json.dumps(data)

        self.login_and_check_http_methods(self.calipso_user.user.username, url,
                                          ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'PATCH'])

        response = self.client.put(url, format='json', content_type='application/json', data=data_str)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        base_url = '/experiments/%s/'
        url = base_url % str(self.calipso_user.user.username)
        response = self.client.get(url, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json().get('results')[1].get('favorite'), True)

