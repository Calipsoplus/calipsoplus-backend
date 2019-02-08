import logging

from apprest.services.resource_docker import CalipsoResourceDockerContainerService
from apprest.services.resource_kubernetes import CalipsoResourceKubernetesService
from apprest.services.resource_static_link import CalipsoResourceStaticLinkService
from apprest.services.resource_virtual_machine import CalipsoResourceVirtualMachineService
from apprest.utils.resources import ResourceType
from apprest.services.quota import CalipsoUserQuotaServices

quota_service = CalipsoUserQuotaServices()
logger = logging.getLogger(__name__)


class CalipsoResource:
    def __init__(self, resource_type):
        self.resource = self.set_resource_by_type(resource_type=resource_type)

    @staticmethod
    def set_resource_by_type(resource_type):
        logger.debug('set_resource_by_type by type (%s)' % resource_type)

        if resource_type == ResourceType.dockercontainer:
            return CalipsoResourceDockerContainerService()
        elif resource_type == ResourceType.kubernetes:
            return CalipsoResourceKubernetesService()
        elif resource_type == ResourceType.virtual_machine:
            return CalipsoResourceVirtualMachineService()
        elif resource_type == ResourceType.static_link:
            return CalipsoResourceStaticLinkService()
        else:
            logger.error('set_resource_by_type by type (%s) not found' % resource_type)
            return None


class GenericCalipsoResourceService(CalipsoResource):
    def __init__(self, resource_type):
        super().__init__(resource_type=resource_type)

    def run_resource(self, username, experiment, public_name):
        logger.debug('run_resource (%s,%s,%s)' % (username, experiment, public_name))
        quota_service.calculate_available_quota(username)
        return self.resource.run_resource(username=username, experiment=experiment, public_name=public_name)

    def rm_resource(self, resource_name):
        logger.debug('rm_resource (%s)' % resource_name)
        return self.resource.rm_resource(resource_name=resource_name)

    def stop_resource(self, resource_name):
        logger.debug('stop_resource (%s)' % resource_name)
        return self.resource.stop_resource(resource_name=resource_name)

    def list_resources(self, username):
        logger.debug('list_resources (%s)' % username)
        return self.resource.list_resources(username=username)
