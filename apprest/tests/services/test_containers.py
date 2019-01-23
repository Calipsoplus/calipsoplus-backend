import logging

from rest_framework.test import APITestCase

from apprest.services.container import CalipsoContainersServices
from apprest.services.quota import CalipsoUserQuotaServices

logger = logging.getLogger(__name__)


class CalipsoContainerServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'images.json', 'quotas.json']

    def setUp(self):
        self.logger.debug('#### setUp CalipsoContainerServiceTestCase : START ####')

        self.containers_service = CalipsoContainersServices()
        self.containers_quota = CalipsoUserQuotaServices()

        self.logger.debug('#### setUp CalipsoContainerServiceTestCase : END ####')

    def test_service_run_stop_rm_container_with_default_quota(self):
        self.logger.debug('#### TEST test_service_run_stop_rm_container_with_default_quota START ####')

        container = self.containers_service.run_container(username='userA', experiment='55555',
                                                          container_public_name='base_jupyter')

        self.assertEqual(len(container.container_id), 64)
        self.assertEqual(container.container_status, 'created')

        self.containers_service.stop_container(container.container_name)
        self.containers_service.rm_container(container.container_name)

        self.logger.debug('#### TEST test_service_run_stop_rm_container_with_default_quota END ####')

    def test_service_run_container_default_quota(self):
        self.logger.debug('#### TEST test_service_run_container_default_quota START ####')

        all_container_responses = []

        quota = self.containers_quota.get_default_quota(username='userA')
        self.logger.debug('quota found .. max:%d' % quota.max_simultaneous)

        for x in range(0, quota.max_simultaneous):
            self.logger.debug('append container %d' % x)
            all_container_responses.append(self.containers_service.run_container(username='userA', experiment=str(x),
                                                                                 container_public_name='base_jupyter'))
            self.assertNotEquals(all_container_responses[x], None)

        # stop all
        for x in range(0, quota.max_simultaneous):
            container = all_container_responses.pop()
            self.containers_service.stop_container(container_name=container.container_name)
            self.containers_service.rm_container(container_name=container.container_name)

        self.logger.debug('#### TEST test_service_run_container_default_quota END ####')