import logging

from rest_framework.test import APITestCase

from apprest.services.container import CalipsoContainersServices

logger = logging.getLogger(__name__)


class CalipsoContainerServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['containers.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.service = CalipsoContainersServices()
        self.logger.debug('#### setUp END ####')

    def test_service_run_stop_rm_container(self):
        self.logger.debug('#### TEST test_service_run_stop_rm_container START ####')

        container = self.service.run_container(username='username', experiment='experiment_id')

        self.assertEqual(len(container.container_id), 64)
        self.assertEqual(container.container_status, 'created')

        self.service.stop_container(container.container_name)
        self.service.rm_container(container.container_name)

        self.logger.debug('#### TEST test_service_run_stop_rm_container END ####')