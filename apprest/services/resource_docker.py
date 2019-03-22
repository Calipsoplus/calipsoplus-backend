import logging
import re
import uuid
import docker

from apprest.models.container import CalipsoContainer
from apprest.services.image import CalipsoAvailableImagesServices

from django.conf import settings

from apprest.services.session import CalipsoSessionsServices
from apprest.utils.exceptions import DockerExceptionNotFound

image_service = CalipsoAvailableImagesServices()
session_service = CalipsoSessionsServices()


class CalipsoResourceDockerContainerService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.client = docker.DockerClient(tls=False, base_url=settings.DOCKER_URL_DAEMON)
            self.logger.debug('Docker deamon has been initialized')
        except Exception as e:
            self.logger.critical("Docker deamon not found.")
            self.logger.critical(e)

    def run_resource(self, username, experiment, public_name):
        """
        Run a new container
        returns a container created
        :param username
        :param experiment
        :param public_name:
        """

        try:
            self.client.ping()
        except Exception as e:
            self.logger.debug('Docker daemon not found.')
            raise DockerExceptionNotFound("Docker daemon not found.")

        image_selected = image_service.get_available_image(public_name=public_name)

        try:
            # generate random values for guacamole credentials
            guacamole_username = uuid.uuid4().hex
            guacamole_password = uuid.uuid4().hex

            vnc_password = 'vncpassword'

            try:
                volume = session_service.get_volumes_from_session(session_number=experiment)

            except Exception as e:
                self.logger.debug('volume not found, set volume to default')
                volume = {"/tmp/results/" + username: {"bind": "/tmp/results/" + username, "mode": "rw"},
                          "/tmp/data/" + username: {"bind": "/tmp/data/" + username, "mode": "ro"}}

            self.logger.debug('volume set to :%s', volume)

            new_container = CalipsoContainer.objects.create(calipso_user=username,
                                                            calipso_experiment=experiment,
                                                            container_id='not created yet',
                                                            container_name='not created yet',
                                                            container_status='busy',
                                                            container_logs="...",
                                                            guacamole_username=guacamole_username,
                                                            guacamole_password=guacamole_password,
                                                            vnc_password=vnc_password,
                                                            public_name=public_name
                                                            )

            docker_container = self.client.containers.run(image=image_selected.image,
                                                          detach=True,
                                                          publish_all_ports=True,
                                                          mem_limit=image_selected.memory,
                                                          memswap_limit=-1,
                                                          cpu_count=image_selected.cpu,
                                                          environment=["PYTHONUNBUFFERED=0"],
                                                          working_dir="/tmp/results/" + username,
                                                          volumes=volume
                                                          )

            new_container.container_id = docker_container.id
            new_container.container_name = docker_container.name
            new_container.container_status = docker_container.status
            new_container.container_info = self.client.api.inspect_container(docker_container.id)

            port = 0
            for key, val in new_container.container_info['NetworkSettings']['Ports'].items():
                bport = int(val[0]['HostPort'])

                if (bport > port):
                    port = bport

            result_er = ""
            for log in docker_container.logs(stream=True):
                result_er = re.findall(image_selected.logs_er, str(log))
                if result_er:
                    break

            if result_er[0] != image_selected.logs_er:
                new_container.host_port = "http://" + settings.REMOTE_MACHINE_IP + ":" + str(port) + "/?" + result_er[0]

            new_container.save()

            self.logger.debug('Return a new container, image:%s', image_selected.image)
            return new_container

        except Exception as e:
            self.logger.error("Run container error")
            self.logger.error(e)
            raise e

    def rm_resource(self, resource_name):
        """
        Remove a container (resource_name)
        :param resource_name: container name to be removed
        """
        self.logger.debug('CalipsoResourceDockerContainerService rm_resource (%s)' % resource_name)

        try:
            self.client.ping()
        except Exception as e:
            self.logger.debug('Docker daemon not found.')
            raise DockerExceptionNotFound("Docker daemon not found.")

        try:
            self.client.api.remove_container(resource_name)

            container = CalipsoContainer.objects.get(container_name=resource_name, container_status='stopped')
            container.container_status = 'removed'
            container.save()

            self.logger.debug('Container ' + resource_name + ' has been removed')

            return container

        except Exception as e:
            self.logger.error("Remove container error")
            self.logger.error(e)
            raise e

    def stop_resource(self, resource_name):
        """
        Stop a container (container_name)
        :param resource_name: container id to be stopped
        :return: none
        """
        self.logger.debug('CalipsoResourceDockerContainerService stop_resource (%s)' % resource_name)

        try:
            self.client.ping()
        except Exception as e:
            self.logger.debug('Docker daemon not found.')
            raise DockerExceptionNotFound("Docker daemon not found.")

        try:
            self.client.api.stop(resource_name)

            container = CalipsoContainer.objects.get(container_name=resource_name, container_status='created')
            container.container_status = 'stopped'
            container.save()

            self.logger.debug('Container ' + resource_name + ' has been stopped')
            return container

        except Exception as e:
            self.logger.error("Stop container error")
            self.logger.error(e)
            raise e

    def list_resources(self, username):
        """
        List all created containers for a user
        :return: list containers
        """
        self.logger.debug('CalipsoResourceDockerContainerService list_resources (%s)' % username)

        try:
            containers = CalipsoContainer.objects.filter(calipso_user=username,
                                                         container_status__in=['created', 'busy'])
            self.logger.debug('List containers from ' + username)
            return containers

        except Exception as e:
            self.logger.error("List container error")
            self.logger.error(e)
            raise e
