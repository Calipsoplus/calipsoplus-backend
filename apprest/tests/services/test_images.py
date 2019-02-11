import logging

from apprest.services.image import CalipsoAvailableImagesServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ImagesServiceTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['resources_type.json', 'images.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.service = CalipsoAvailableImagesServices()
        self.logger.debug('#### setUp END ####')

    def test_get_all_images(self):
        self.logger.debug('#### TEST get_all_facilities START ####')

        # get_all_images
        all_images = self.service.get_all_images()

        self.assertEqual(len(all_images), 5)
        self.logger.debug('#### TEST get_all_facilities END ####')

