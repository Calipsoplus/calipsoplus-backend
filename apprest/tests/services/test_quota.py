import logging

from rest_framework.exceptions import NotFound
from rest_framework.test import APITestCase

from apprest.models import CalipsoAvailableImages, CalipsoResourcesType
from apprest.services.resources import GenericCalipsoResourceService
from apprest.utils.exceptions import QuotaCpuExceeded, QuotaMemoryExceeded, QuotaHddExceeded, \
    QuotaMaxSimultaneousExceeded

logger = logging.getLogger(__name__)


class CalipsoUserQuotaTestCase(APITestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'images.json', 'quotas.json', 'users_experiments.json', 'experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp CalipsoUserQuotaTestCase : START ####')

        self.public_name = 'base_jupyter'
        image_selected = CalipsoAvailableImages.objects.get(public_name=self.public_name)
        try:
            resource_type = CalipsoResourcesType.objects.get(pk=image_selected.resource_type.id)
        except Exception as e:
            logger.debug("CalipsoResourcesType.objects.get e:%s" % e)
            raise NotFound

        self.resource_service = GenericCalipsoResourceService(resource_type.resource_type)

        self.logger.debug('#### setUp CalipsoUserQuotaTestCase : END ####')

    def test_max_resources(self):
        self.logger.debug('#### TEST test_max_resources START ####')

        container_1 = self.resource_service.run_resource(username='userA', experiment='2018091622',
                                                         public_name=self.public_name)
        container_2 = self.resource_service.run_resource(username='userA', experiment='2018091632',
                                                         public_name=self.public_name)
        container_3 = self.resource_service.run_resource(username='userA', experiment='2018091634',
                                                         public_name=self.public_name)

        with self.assertRaisesMessage(QuotaMaxSimultaneousExceeded, 'Max machines exceeded'):
            self.resource_service.run_resource(username='userA', experiment='2018091625',
                                               public_name=self.public_name)

        self.resource_service.stop_resource(resource_name=container_1.container_name)
        self.resource_service.rm_resource(resource_name=container_1.container_name)

        self.resource_service.stop_resource(resource_name=container_2.container_name)
        self.resource_service.rm_resource(resource_name=container_2.container_name)

        self.resource_service.stop_resource(resource_name=container_3.container_name)
        self.resource_service.rm_resource(resource_name=container_3.container_name)

        active_containers = self.resource_service.list_resources(username='userA')
        self.assertEqual(len(active_containers), 0)

    def test_quota_cpu(self):
        self.logger.debug('#### TEST test_quota_cpu START ####')

        resource_1 = self.resource_service.run_resource(username='userB', experiment='2018091622',
                                                        public_name=self.public_name)
        resource_2 = self.resource_service.run_resource(username='userB', experiment='2018091632',
                                                        public_name=self.public_name)

        with self.assertRaisesMessage(QuotaCpuExceeded, 'Max cpus exceeded'):
            self.resource_service.run_resource(username='userB', experiment='2018091634',
                                               public_name=self.public_name)

        self.resource_service.stop_resource(resource_name=resource_1.container_name)
        self.resource_service.rm_resource(resource_name=resource_1.container_name)

        self.resource_service.stop_resource(resource_name=resource_2.container_name)
        self.resource_service.rm_resource(resource_name=resource_2.container_name)

        active_containers = self.resource_service.list_resources(username='userB')
        self.assertEqual(len(active_containers), 0)

    def test_quota_memory(self):
        self.logger.debug('#### TEST test_quota_memory START ####')

        resource_a = self.resource_service.run_resource(username='userC', experiment='2018091622',
                                                         public_name=self.public_name)
        resource_b = self.resource_service.run_resource(username='userC', experiment='2018091632',
                                                         public_name=self.public_name)

        with self.assertRaisesMessage(QuotaMemoryExceeded, 'Max memory exceeded'):
            self.resource_service.run_resource(username='userC', experiment='2018091633',
                                               public_name=self.public_name)

        self.resource_service.stop_resource(resource_name=resource_a.container_name)
        self.resource_service.rm_resource(resource_name=resource_a.container_name)

        self.resource_service.stop_resource(resource_name=resource_b.container_name)
        self.resource_service.rm_resource(resource_name=resource_b.container_name)

        active_containers = self.resource_service.list_resources(username='userC')
        self.assertEqual(len(active_containers), 0)

    def test_quota_hdd(self):
        self.logger.debug('#### TEST test_quota_hdd START ####')

        container_a = self.resource_service.run_resource(username='userD', experiment='2018091622',
                                                         public_name=self.public_name)
        container_b = self.resource_service.run_resource(username='userD', experiment='2018091632',
                                                         public_name=self.public_name)

        with self.assertRaisesMessage(QuotaHddExceeded, 'Max hdd exceeded'):
            self.resource_service.run_resource(username='userD', experiment='2018091633',
                                               public_name=self.public_name)

        self.resource_service.stop_resource(resource_name=container_a.container_name)
        self.resource_service.rm_resource(resource_name=container_a.container_name)

        self.resource_service.stop_resource(resource_name=container_b.container_name)
        self.resource_service.rm_resource(resource_name=container_b.container_name)

        active_containers = self.resource_service.list_resources(username='userD')
        self.assertEqual(len(active_containers), 0)
