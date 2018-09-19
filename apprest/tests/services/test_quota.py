import logging

from rest_framework.test import APITestCase

from apprest.services.container import CalipsoContainersServices
from apprest.utils.exceptions import QuotaCpuExceeded, QuotaMemoryExceeded, QuotaHddExceeded

logger = logging.getLogger(__name__)


class CalipsoUserQuotaTestCase(APITestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'images.json', 'quotas.json']

    def setUp(self):
        self.logger.debug('#### setUp CalipsoContainerServiceTestCase : START ####')

        self.containers_service = CalipsoContainersServices()

        self.logger.debug('#### setUp CalipsoContainerServiceTestCase : END ####')

    def test_quota_cpu(self):
        self.logger.debug('#### TEST test_quota_cpu START ####')

        container_a = self.containers_service.run_container(username='userB', experiment='EXPERIMENT S/N')
        container_b = self.containers_service.run_container(username='userB', experiment='EXPERIMENT S/N')

        with self.assertRaisesMessage(QuotaCpuExceeded, 'Max cpus exceeded'):
            self.containers_service.run_container(username='userB', experiment='EXPERIMENT S/N')

        self.containers_service.stop_container(container_name=container_a.container_name)
        self.containers_service.rm_container(container_name=container_a.container_name)

        self.containers_service.stop_container(container_name=container_b.container_name)
        self.containers_service.rm_container(container_name=container_b.container_name)

        active_containers = self.containers_service.list_container(username='userA')
        self.assertEqual(len(active_containers), 0)

    def test_quota_memory(self):
        self.logger.debug('#### TEST test_quota_cpu START ####')

        container_a = self.containers_service.run_container(username='userC', experiment='EXPERIMENT S/N')
        container_b = self.containers_service.run_container(username='userC', experiment='EXPERIMENT S/N')

        with self.assertRaisesMessage(QuotaMemoryExceeded, 'Max memory exceeded'):
            self.containers_service.run_container(username='userC', experiment='EXPERIMENT S/N')

        self.containers_service.stop_container(container_name=container_a.container_name)
        self.containers_service.rm_container(container_name=container_a.container_name)

        self.containers_service.stop_container(container_name=container_b.container_name)
        self.containers_service.rm_container(container_name=container_b.container_name)

        active_containers = self.containers_service.list_container(username='userA')
        self.assertEqual(len(active_containers), 0)

    def test_quota_hdd(self):
        self.logger.debug('#### TEST test_quota_hdd START ####')

        container_a = self.containers_service.run_container(username='userD', experiment='EXPERIMENT S/N')
        container_b = self.containers_service.run_container(username='userD', experiment='EXPERIMENT S/N')

        with self.assertRaisesMessage(QuotaHddExceeded, 'Max hdd exceeded'):
            self.containers_service.run_container(username='userD', experiment='EXPERIMENT S/N')

        self.containers_service.stop_container(container_name=container_a.container_name)
        self.containers_service.rm_container(container_name=container_a.container_name)

        self.containers_service.stop_container(container_name=container_b.container_name)
        self.containers_service.rm_container(container_name=container_b.container_name)

        active_containers = self.containers_service.list_container(username='userA')
        self.assertEqual(len(active_containers), 0)