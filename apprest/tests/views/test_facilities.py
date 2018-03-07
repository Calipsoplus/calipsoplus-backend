import json
from rest_framework import status

import logging

from apprest.models.facilities import CalipsoFacility
from apprest.services.facility import CalipsoFacilityServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class FacilityViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.service = CalipsoFacilityServices()
        self.facility_alba = CalipsoFacility.objects.create(name='ALBA', description='Cells Alba syncotron', url ='https://calipsoplus.cells.es/')

        self.logger.debug('#### setUp END ####')

    def test_get_all_facilities(self):
        self.logger.debug('#### TEST get_all_facilitites START ####')

        url = '/facilities/all/'

        # Should return status 200 if everything goes fine

        self.logger.debug('# TEST URL --> %s' % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug('# response.content --> %s' % response.content)

        json_content = json.loads(response.content.decode("utf-8"))
        self.logger.debug('# RESPONSE --> %s' % json_content)
        self.assertIsInstance(json_content, list)
        self.assertGreater(len(json_content), 0)

        self.logger.debug('#### TEST get time_entry by pk END ####')

