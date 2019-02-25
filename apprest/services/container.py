import logging
from apprest.models import CalipsoContainer


class CalipsoContainersServices:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

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

        try:
            containers = CalipsoContainer.objects.filter(calipso_user=username,
                                                         container_status__in=['created', 'busy'])
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
            containers = CalipsoContainer.objects.filter(container_status__in=['created', 'busy'])
            return containers

        except Exception as e:
            self.logger.error('Unable to list all containers')
            self.logger.error(e)
            raise e
