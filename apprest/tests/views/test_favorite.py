import logging

from rest_framework import status

from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class FavoriteExperimentViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users_experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.logger.debug('#### setUp END ####')

    def test_swap_favorite(self):
        response = self.client.put('/favorite/4/', {'favorite': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

