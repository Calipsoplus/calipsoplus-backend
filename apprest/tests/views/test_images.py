import json

from django.contrib.auth.models import User
from rest_framework import status

import logging

from apprest.services.image import CalipsoAvailableImagesServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ImageViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['images.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.test_user = User.objects.create_user(**self.credentials)

        self.service = CalipsoAvailableImagesServices()

        self.logger.debug('#### setUp END ####')

    def test_get_all_images(self):
        self.logger.debug('#### TEST test_get_all_images START ####')

        url = '/login/'
        data_str = json.dumps(self.credentials)
        response = self.client.post(url, format='json', content_type='application/json', data=data_str)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/images/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_content = json.loads(response.content.decode("utf-8"))

        self.assertIsInstance(json_content, list)
        self.assertGreater(len(json_content), 0)

        self.logger.debug('#### TEST test_get_all_images END ####')