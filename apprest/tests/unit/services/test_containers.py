import logging

from rest_framework.test import APITestCase

from apprest.services.container import CalipsoContainersServices

logger = logging.getLogger(__name__)


class CalipsoContainerServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'containers.json']

    def setUp(self):
        self.logger.debug('#### setUp CalipsoContainerServiceTestCase : START ####')
        self.containers_service = CalipsoContainersServices()
        self.logger.debug('#### setUp CalipsoContainerServiceTestCase : END ####')

    def test_get_containers_list(self):
        self.logger.debug('#### TEST test_get_containers_list START ####')

        containers_list = self.containers_service.list_container(username='userA')
        self.assertEqual(len(containers_list), 3)
        self.logger.debug('#### TEST test_get_containers_list END ####')

    def test_get_total_num_cpus_used(self):
        self.assertEqual(self.containers_service.get_total_num_cpus_used(), 7)

    def test_get_total_memory_allocated(self):
        self.assertEqual(self.containers_service.get_total_memory_allocated(), '26.0G')

    def test_get_total_hdd_allocated(self):
        self.assertEqual(self.containers_service.get_total_hdd_allocated(), '70.0G')
