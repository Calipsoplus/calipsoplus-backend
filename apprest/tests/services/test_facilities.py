from rest_framework.test import APITestCase

import logging

from apprest.models.facilities import CalipsoFacility
from apprest.services.facility import CalipsoFacilityServices

logger = logging.getLogger(__name__)


class FacilityServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['facilities.json']


    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.service = CalipsoFacilityServices()
        self.facilities = ['ALBA-CELLS', 'HRZ-2', 'RESNO-1']

        self.logger.debug('#### setUp END ####')

    def test_get_all_facilities(self):
        self.logger.debug('#### TEST get_all_facilities START ####')

        # create facilities
        for facility in self.facilities:
            CalipsoFacility.create(name=facility, description='facility for test', url='http://calipsoplus.cells.es')

        # get_all_facilities
        all_facilities = self.service.get_all_facilities()
        self.assertEqual(len(all_facilities), len(self.facilities) + 2)  # two from fixtures
        self.logger.debug('#### TEST get_all_facilities END ####')
