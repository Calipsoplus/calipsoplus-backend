import logging
import pdb
import uuid

import docker

from apprest.models.container import CalipsoContainer
from calipsoplus.settings import DOCKER_URL_DAEMON

DOCKER_IMAGE = "consol/centos-xfce-vnc:latest"


class CalipsoContainersServices:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.client = docker.DockerClient(tls=False, base_url=DOCKER_URL_DAEMON)
            self.logger.info('Docker deamon has been initialized')
        except Exception as e:
            self.logger.critical("Docker deamon not found. %s" % e)

    def run_container(self, username, experiment):
        """
        Run a new container
        returns a container created
        """
        self.logger.info('Attempting to run a new container')
        # ports = {'5901/tcp': 5901} to assign specific port

        try:

            # generate random values for guacamole credentials
            guacamole_username = uuid.uuid4().hex
            guacamole_password = uuid.uuid4().hex

            vnc_password = 'vncpassword'

            # add to the img vncpassword
            # select img

            docker_container = self.client.containers.run(DOCKER_IMAGE,
                                                          # ports=ports,
                                                          detach=True,
                                                          publish_all_ports=True)

            self.logger.info('Container ' + docker_container.name + ' has been created')

            new_container = CalipsoContainer.objects.create(calipso_user=username,
                                                            calipso_experiment=experiment,
                                                            container_id=docker_container.id,
                                                            container_name=docker_container.name,
                                                            container_status=docker_container.status,
                                                            container_info=self.client.api.inspect_container(
                                                                docker_container.id),
                                                            container_logs="...",
                                                            guacamole_username=guacamole_username,
                                                            guacamole_password=guacamole_password,
                                                            vnc_password=vnc_password
                                                            )

            return new_container

        except Exception as e:
            self.logger.error(e)

            raise e

    def rm_container(self, container_name):
        """
        Remove a container (container_name)
        :param container_name: container name to be removed
        """
        self.logger.info('Attempting to remove container %s' % container_name)

        try:
            self.client.api.remove_container(container_name)

            container = CalipsoContainer.objects.get(container_name=container_name)
            container.container_status = 'removed'
            container.save()

            self.logger.info('Container ' + container_name + ' has been removed')

            return container

        except Exception as e:
            self.logger.error(e)
            return e

    def stop_container(self, container_name):
        """
        Stop a container (container_name)
        :param container_name: container id to be stopped
        :return: none
        """
        self.logger.info('Attempting to stop a container %s' % container_name)

        try:
            self.client.api.stop(container_name)

            container = CalipsoContainer.objects.get(container_name=container_name)
            container.container_status = 'stopped'
            container.save()

            self.logger.info('Container ' + container_name + ' has been stopped')

            return container

        except Exception as e:
            self.logger.error(e)
            return e

    def list_container(self, username):
        """
        List all created containers for a user
        :return: list containers
        """
        self.logger.info('Attempting to list containers from calipso user:' + username)

        try:
            containers = CalipsoContainer.objects.filter(calipso_user=username, container_status='created')
            self.logger.info('List containers from ' + username)

            return containers

        except CalipsoContainer.DoesNotExist as dne:
            self.logger.error(dne)
            return dne