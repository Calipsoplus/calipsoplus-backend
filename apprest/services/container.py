import logging

from django.db.models import Sum

from apprest.models import CalipsoContainer
from apprest.services.resource_kubernetes import CalipsoResourceKubernetesService


class CalipsoContainersServices:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    # Temporary fix for updating the container status as there is a delay when kubernetes creates the container
    # and when it is in the 'Running' stage
    def update_container_status(self):
        service = CalipsoResourceKubernetesService()
        containers = CalipsoContainer.objects.filter(container_status__in=['Pending'])
        if len(containers) == 0:
            return
        for container in containers:
            if container.container_status == 'Pending':
                status = service.get_pod_status(container.container_name)
                CalipsoContainer.objects.filter(id=container.id).update(container_status=status)
                self.logger.debug('Container %s status updated' % container.id)

    def get_container_by_id(self, cid):
        """
        Return a container with a given id
        :return: single container
        """

        self.logger.debug('Attempting to get container with id :' + cid)
        try:
            container = CalipsoContainer.objects.get(id=cid)
            self.logger.debug('Returning container ' + cid)
            return container

        except Exception as e:
            self.logger.error("Returning container error")
            self.logger.error(e)
            raise e

    def list_container(self, username):
        """
        List all created containers for a user
        :return: list containers
        """
        self.logger.debug('Attempting to list containers from calipso user:' + username)
        self.update_container_status()
        try:
            containers = CalipsoContainer.objects.filter(calipso_user=username,
                                                         container_status__in=['created', 'busy', 'Running', 'Pending'])
            self.logger.debug('List containers from ' + username)
            return containers

        except Exception as e:
            self.logger.error("List container error")
            self.logger.error(e)
            raise e

    def list_all_containers(self):
        """
        List all of the created containers
        :return: list containers
        """
        self.logger.debug('Listing all containers')

        try:
            containers = CalipsoContainer.objects.all()
            return containers

        except Exception as e:
            self.logger.error('Unable to list all containers')
            self.logger.error(e)
            raise e

    def list_all_active_containers(self):
        """
        List all of the containers currently active
        :return: list containers
        """
        self.logger.debug('Listing all active containers')

        try:
            containers = CalipsoContainer.objects.filter(container_status__in=['created', 'busy', 'Running'])
            return containers

        except Exception as e:
            self.logger.error('Unable to list all containers')
            self.logger.error(e)
            raise e

    def get_total_num_cpus_used(self):
        """
        Get the total number of CPUs being used by all active containers
        :return: integer num_cpus_used
        """
        num_cpus_used = self.list_all_active_containers().aggregate(Sum('num_cpus'))['num_cpus__sum']
        return num_cpus_used

    def get_total_memory_allocated(self):
        """
        Get the total amount of memory being used by all active containers
        :return: double total_memory_allocated
        """
        total_memory_allocated = self.list_all_active_containers().aggregate(Sum('memory_allocated'))[
            'memory_allocated__sum']
        return str(total_memory_allocated) + 'G'

    def get_total_hdd_allocated(self):
        """
        Get the total amount of storage being used by all active containers
        :return: double total_hdd_allocated
        """
        total_hdd_allocated = self.list_all_active_containers().aggregate(Sum('hdd_allocated'))[
            'hdd_allocated__sum']
        return str(total_hdd_allocated) + 'G'
