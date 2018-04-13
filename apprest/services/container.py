import logging

from apprest.models.container import CalipsoContainer


class CalipsoContainerServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_user_containers(self,user_id):
        self.logger.debug('Getting all containers from user')
        try:
            containers = CalipsoContainer.objects.get(calipso_user_id=user_id).containers.all()
            self.logger.debug('get_containers got')
            return containers
        except Exception as e:
            self.logger.error(e)
            raise e

    def delete(self, container):
        if container is None:
            error_message = 'Container could not be None'
            self.logger.error(error_message)
            raise Exception(error_message)
        try:
            container.delete()
        except Exception as e:
            self.logger.error(e)
            raise e
