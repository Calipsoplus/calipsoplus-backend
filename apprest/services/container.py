import logging
import pdb

import docker

from apprest.models.container import CalipsoContainer

CALIPSO_EXPERIMENT = "A/7889"
CALIPSO_USER_NAME = "acampsm"
DOCKER_IMAGE = "consol/centos-xfce-vnc:latest"
DOCKER_URL_DAEMON = "tcp://192.168.33.13:2375"


class CalipsoContainersServices:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.client = docker.DockerClient(tls=False, base_url=DOCKER_URL_DAEMON)
            self.logger.info('Docker deamon has been initialized')
        except Exception as e:
            self.logger.critical("Docker deamon not found. %s" % e)

    def run_container(self):
        """
        Run a new container
        returns a container created
        """
        self.logger.info('Attempting to run a new container')
        # ports = {'5901/tcp': 5901} to assign specific port

        try:

            # TODO: generate random values for guacamole credentials
            guacamole_username = 'alexcamps'
            guacamole_password = 'password'
            vnc_password = 'vncpassword'

            # add to the img vncpassword
            # select img

            docker_container = self.client.containers.run(DOCKER_IMAGE,
                                                          # ports=ports,
                                                          detach=True,
                                                          publish_all_ports=True)

            self.logger.info('Container ' + docker_container.name + ' has been created')

            new_container = CalipsoContainer.objects.create(calipso_user=CALIPSO_USER_NAME,
                                                            calipso_experiment=CALIPSO_EXPERIMENT,
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

    def rm_container(self, container_id):
        """
        Remove a container (container_id)
        :param container_id: container id to be removed
        """
        self.logger.info('Attempting to remove container %s' % container_id)

        try:
            self.client.api.remove_container(container_id)
            self.logger.info('Container ' + container_id + ' has been created')
            return "container removed"

        except Exception as e:
            return e

    def stop_container(self, container_id):
        """
        Stop a container (container_id)
        :param container_id: container id to be stopped
        :return: none
        """
        self.logger.info('Attempting to stop a container %s' % container_id)

        try:
            self.client.api.stop(container_id)
            self.logger.info('Container ' + container_id + ' has been stopped')
            return "container stopped"

        except Exception as e:
            return e
