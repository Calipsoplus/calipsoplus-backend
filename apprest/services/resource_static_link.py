import logging
import uuid

from apprest.models import CalipsoContainer, CalipsoUser
from apprest.services.image import CalipsoAvailableImagesServices

image_service = CalipsoAvailableImagesServices()


class CalipsoResourceStaticLinkService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('CalipsoResourceStaticLinkService initialized')

    def run_resource(self, username, experiment, public_name):
        self.logger.debug('CalipsoResourceStaticLinkService run_resource')
        self.logger.debug('run_resource(static_link) public_name=%s' % public_name)
        user = CalipsoUser.objects.get(user__username=username)
        try:
            image_selected = image_service.get_available_image(public_name=public_name)

            new_container = CalipsoContainer.objects.create(calipso_user=user,
                                                            calipso_experiment=experiment,
                                                            container_id=uuid.uuid4().hex,
                                                            container_name=uuid.uuid4(),
                                                            container_status='created',
                                                            container_logs="...",
                                                            guacamole_username="",
                                                            guacamole_password="",
                                                            vnc_password="",
                                                            public_name=public_name,
                                                            host_port=image_selected.image
                                                            )

            new_container.save()
            return new_container

        except Exception as e:
            self.logger.debug('Docker daemon not found.')
            raise e

    def rm_resource(self, resource_name):
        self.logger.debug('CalipsoResourceStaticLinkService rm_resource')
        try:
            container = CalipsoContainer.objects.get(container_name=resource_name, container_status='stopped')
            container.container_status = 'removed'
            container.save()
            return container
        except Exception as e:
            self.logger.error("rm_static_link error")
            self.logger.error(e)
            raise e

    def stop_resource(self, resource_name):
        self.logger.debug('CalipsoResourceStaticLinkService stop_resource')
        try:
            container = CalipsoContainer.objects.get(container_name=resource_name, container_status='created')
            container.container_status = 'stopped'
            container.save()
            return container
        except Exception as e:
            self.logger.error("stop_static_link error")
            self.logger.error(e)
            raise e

    def list_resources(self, username):
        self.logger.debug('CalipsoResourceStaticLinkService list_resources')
        return NotImplemented
