import logging

from rest_framework import status
from rest_framework.test import APITestCase

from apprest.services.container import CalipsoContainersServices
from calipsoplus.settings import MAX_CONTAINER_PER_USER

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

    def test_service_run_container(self):
        self.logger.debug('#### TEST test_service_run_container START ####')

        all_container_responses = []
        for x in range(0, MAX_CONTAINER_PER_USER):
            all_container_responses.append(self.service.run_container(username='username', experiment=str(x)))
            self.assertNotEquals(all_container_responses[x], None)

        last_fail_container = self.service.run_container(username='username', experiment='999')
        self.assertEqual(last_fail_container, None)

        # stop all
        for x in range(0, MAX_CONTAINER_PER_USER):
            container = all_container_responses.pop()
            self.service.stop_container(container_name=container.container_name)

        self.logger.debug('#### TEST test_service_run_container END ####')