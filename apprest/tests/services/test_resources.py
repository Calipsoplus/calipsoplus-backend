import logging

from django.contrib.auth.models import User

from apprest.services.resources import GenericCalipsoResourceService
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ResourceServiceTestCase(CalipsoTestCase):
    fixtures = ['users.json', 'images.json', 'quotas.json']

    def setUp(self):
        self.logger.debug('#################### setup test ResourceServiceTestCase  ####')
        self.username = User.objects.get(username='userA').username

    def test_docker_resource_service(self):
        self.logger.debug('#################### test_docker_resource_service ####')

        resource_service = GenericCalipsoResourceService('docker_container')

        resource = resource_service.run_resource(username=self.username, experiment='55555',
                                                 public_name='base_jupyter')

        self.assertEqual(len(resource.container_id), 64)
        self.assertEqual(resource.container_status, 'created')

        resources_list = resource_service.list_resources(username=self.username)

        self.assertEqual(len(resources_list), 1)

        resource_service.stop_resource(resource_name=resource.container_name)
        resource_service.rm_resource(resource_name=resource.container_name)

        resources_list = resource_service.list_resources(username=self.username)

        self.assertEqual(len(resources_list), 0)

    def test_kubernetes_resource_service(self):
        self.logger.debug('#################### test_kubernetes_resource_service ####')

        resource_service = GenericCalipsoResourceService('kubernetes')

        resource = resource_service.run_resource(username=self.username, experiment='55555',
                                                 public_name='kubernetes_jupyter')

        self.assertEqual(resource, NotImplemented)

    def test_virtual_machine_resource_service(self):
        self.logger.debug('#################### test_virtual_machine_resource_service ####')

        resource_service = GenericCalipsoResourceService('virtual_machine')

        resource = resource_service.run_resource(username=self.username, experiment='55555',
                                                 public_name='vm_jupyter')

        self.assertEqual(resource, NotImplemented)

    def test_static_link_resource_service(self):
        self.logger.debug('#################### test_static_link_resource_service ####')

        resource_service = GenericCalipsoResourceService('static_link')

        resource = resource_service.run_resource(username=self.username, experiment='55555',
                                                 public_name='static_yahoo')

        self.assertEqual(resource.host_port, "http://www.yahoo.es")

