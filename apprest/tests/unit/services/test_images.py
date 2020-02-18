import logging

from apprest.services.container import CalipsoContainersServices
from apprest.services.image import CalipsoAvailableImagesServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ImagesServiceTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'containers.json', 'images.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.service = CalipsoAvailableImagesServices()
        self.logger.debug('#### setUp END ####')

    def test_get_all_images(self):
        self.logger.debug('#### TEST get_all_facilities START ####')

        # get_all_images
        all_images = self.service.get_all_images()

        self.assertEqual(len(all_images), 6)

        self.logger.debug('#### TEST get_all_facilities END ####')

    def test_total_image_usage(self):

        image_usage = CalipsoAvailableImagesServices.get_total_image_usage()
        # Get number of containers using image with pk 1
        self.assertEqual(image_usage[0].num_containers, 1)
        # Get number of containers using image with pk 2
        self.assertEqual(image_usage[1].num_containers, 2)
