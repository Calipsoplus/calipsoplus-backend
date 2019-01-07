import logging
import docker
import docker.errors

from django.conf import settings
from rest_framework.exceptions import NotFound
from django.db import IntegrityError

from apprest.models.image import CalipsoAvailableImages
from apprest.models.quota import CalipsoUserQuota


class CalipsoAvailableImagesServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.client = docker.DockerClient(tls=False, base_url=settings.DOCKER_URL_DAEMON)
            self.logger.debug('Docker deamon has been initialized')
        except Exception as e:
            self.logger.critical("Docker deamon not found.")
            self.logger.critical(e)

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
        self.logger.debug('Attempting to add new image %s' % public_name)
        try:
            new_image = CalipsoAvailableImages(public_name=public_name, image=image, docker_daemon='tcp://:2375',
                                           host_domain='', port_hook=port_hook, logs_er=logs_er,
                                           protocol=protocol, cpu=cpu, memory=memory, hdd=hdd)
            try:
                self.logger.debug(str(image))
                self.client.images.get_registry_data(str(image))
                new_image.save()
                self.logger.debug('Successfully added new image: %s' % public_name)
            except IntegrityError as integrityError:
                if 'UNIQUE constraint failed' in integrityError.args[0]:
                    self.logger.error('%s already exists' % public_name)
                else:
                    self.logger.error(integrityError)
            except docker.errors.APIError:
                # Will be docker.errors.APIError meaning image not found
                self.logger.error("This image does not exist in the attached repository(ies)")
                self.logger.error("%s has not been added" % public_name)

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
                max_cpu += image.cpu
                max_memory += int(image.memory[:-1])
                max_hdd += int(image.hdd[:-1])

            quota = CalipsoUserQuota()
            quota.max_simultaneous = max_simultaneous
            quota.memory = "%dG" % max_memory
            quota.cpu = max_cpu
            quota.hdd = "%dG" % max_hdd

            return quota

        except Exception as e:
            self.logger.error('Error to get calipso_user from quota user:%s' % username)
            self.logger.debug(e)
            raise NotFound
