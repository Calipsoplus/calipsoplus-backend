import logging

from rest_framework import status

from apprest.tests.utils import CalipsoTestCase


class UmbrellaViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

    def test_get_umbrella_session(self):
        url = '/umbrella/session/'

        response = self.client.get(url)
        msg = response.json().get('msg')

        self.assertEqual(msg, 'session not found')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)