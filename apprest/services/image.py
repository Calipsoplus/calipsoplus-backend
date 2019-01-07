import logging

from rest_framework.exceptions import NotFound

from apprest.models.image import CalipsoAvailableImages
from apprest.models.quota import CalipsoUserQuota


class CalipsoAvailableImagesServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_available_image(self, public_name):
        self.logger.debug('Getting one get_available_image: %s' % public_name)
        try:
            selected_image = CalipsoAvailableImages.objects.get(public_name=public_name)
            self.logger.debug('Available image got')
            return selected_image

        except Exception as e:
            self.logger.error("%s not found." % public_name)
            self.logger.error(e)
            raise NotFound

    def get_all_images(self):
        self.logger.debug('Getting all available images')
        try:
            images = CalipsoAvailableImages.objects.all()
            self.logger.debug("Retrieved all images")
            return images
        except Exception as e:
            self.logger.error(e)
            raise Exception

    def add_new_image(self, public_name, image, port_hook, logs_er, protocol, cpu, memory, hdd):
        self.logger.debug('Add new image')
        try:
            image = CalipsoAvailableImages(public_name=public_name, image=image, docker_daemon='tcp://:2375',
                                           host_domain='', port_hook=port_hook, logs_er=logs_er,
                                           protocol=protocol, cpu=cpu, memory=memory, hdd=hdd)
            image.save()
            self.logger.debug('Added new image: %s' % public_name)
        except Exception as e:
            self.logger.error(e)

    def modify_image(self, public_name, image, port_hook, logs_er, protocol, cpu, memory, hdd):
        self.logger.debug('Modifying image %s' % public_name)
        try:
            selected_image = self.get_available_image(public_name)
            selected_image.image = image
            selected_image.port_hook = port_hook
            selected_image.logs_er = logs_er
            selected_image.protocol = protocol
            selected_image.cpu = cpu
            selected_image.memory = memory
            selected_image.hdd = hdd

            selected_image.save()
            self.logger.debug('Image: %s has been updated' % public_name)
        except Exception as e:
            self.logger.error(e)

    def delete_image(self, public_name):
        self.logger.debug('Attempting to delete image %s' % public_name)
        try:
            selected_image = self.get_available_image(public_name)
            selected_image.delete()
            self.logger.debug('Image %s successfully deleted' % public_name)
        except Exception as e:
            self.logger.error(e)


    def get_sum_containers_quota(self, username):
        self.logger.debug('Getting get_sum_containers_quota quota')

        from apprest.services.container import CalipsoContainersServices
        container_service = CalipsoContainersServices()

        try:
            list_of_containers = container_service.list_container(username=username)

            max_simultaneous = 0
            max_cpu = 0
            max_memory = 0
            max_hdd = 0

            for container in list_of_containers:
                image = self.get_available_image(public_name=container.public_name)
                max_simultaneous += 1
                max_cpu += image[0].cpu
                max_memory += int(image[0].memory[:-1])
                max_hdd += int(image[0].hdd[:-1])

            quota = (CalipsoUserQuota(),)
            quota[0].max_simultaneous = max_simultaneous
            quota[0].memory = "%dG" % max_memory
            quota[0].cpu = max_cpu
            quota[0].hdd = "%dG" % max_hdd

            return quota

        except Exception as e:
            self.logger.error('Error to get calipso_user from quota user:%s' % username)
            self.logger.debug(e)
            raise NotFound