import logging
import uuid

import docker

from apprest.models.container import CalipsoContainer
from apprest.services.image import CalipsoAvailableImagesServices

from django.conf import settings

from apprest.services.quota import CalipsoUserQuotaServices
from apprest.utils.exceptions import QuotaMaxSimultaneousExceeded, QuotaHddExceeded, QuotaMemoryExceeded, \
    QuotaCpuExceeded

quota_service = CalipsoUserQuotaServices()
image_service = CalipsoAvailableImagesServices()

default_public_image_name = "base_image"


class CalipsoContainersServices:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.client = docker.DockerClient(tls=False, base_url=settings.DOCKER_URL_DAEMON)
            self.logger.debug('Docker deamon has been initialized')
        except Exception as e:
            self.logger.critical("Docker deamon not found. %s" % e)

    def run_container(self, username, experiment):
        """
        Run a new container
        returns a container created
        """

        max_simultaneous = 0
        max_cpu = 0
        max_memory = 0
        max_hdd = 0

        self.logger.debug('Attempting to run a new container')
        # ports = {'5901/tcp': 5901} to assign specific port

        list_of_containers = self.list_container(username=username)

        for container in list_of_containers:
            image = image_service.get_available_image(public_name=container.public_name)[0]
            max_simultaneous += 1
            max_cpu += image.cpu
            max_memory += int(image.memory[:-1])
            max_hdd += int(image.hdd[:-1])

        try:
            quota_per_user = quota_service.get_default_quota(username=username)[0]
        except Exception as e:
            self.logger.debug('ERRROR :%s' % e)

        self.logger.debug("num_containers_per_user = %d" % len(list_of_containers))

        if max_simultaneous >= quota_per_user.max_simultaneous:
            self.logger.debug(
                'user:%s used:%d > quota.max:%d' % (username, max_simultaneous, quota_per_user.max_simultaneous))
            raise QuotaMaxSimultaneousExceeded("Max machines exceeded")

        if max_cpu >= quota_per_user.cpu:
            self.logger.debug('user:%s cpu_used:%d > quota.max_cpu:%d' % (username, max_cpu, quota_per_user.cpu))
            raise QuotaCpuExceeded("Max cpus exceeded")

        if max_memory >= int(quota_per_user.memory[:-1]):
            self.logger.debug(
                'user:%s max_ram_used:%dG > quota_user.max_ram:%s' % (username, max_memory, quota_per_user.memory))
            raise QuotaMemoryExceeded("Max memory exceeded")

        if max_hdd >= int(quota_per_user.hdd[:-1]):
            self.logger.debug('user:%s max_hdd:%dG quota.max_hdd:%s' % (username, max_hdd, quota_per_user.hdd))
            raise QuotaHddExceeded("Max hdd exceeded")

        image_selected = image_service.get_available_image(public_name=default_public_image_name)[0]

        try:
            # generate random values for guacamole credentials
            guacamole_username = uuid.uuid4().hex
            guacamole_password = uuid.uuid4().hex

            vnc_password = 'vncpassword'
            # add to the img vncpassword
            # select img

            new_container = CalipsoContainer.objects.create(calipso_user=username,
                                                            calipso_experiment=experiment,
                                                            container_id='not created yet',
                                                            container_name='not created yet',
                                                            container_status='busy',
                                                            container_logs="...",
                                                            guacamole_username=guacamole_username,
                                                            guacamole_password=guacamole_password,
                                                            vnc_password=vnc_password,
                                                            public_name=image_selected.public_name
                                                            )

            docker_container = self.client.containers.run(image=image_selected.image,
                                                          # ports=ports,
                                                          detach=True,
                                                          publish_all_ports=True,
                                                          mem_limit=image_selected.memory,
                                                          memswap_limit=-1,
                                                          cpu_count=image_selected.cpu
                                                          )
            """
            storage_opt={'size': '120G'})
            """

            new_container.container_id = docker_container.id
            new_container.container_name = docker_container.name
            new_container.container_status = docker_container.status
            new_container.container_info = self.client.api.inspect_container(docker_container.id)

            port = new_container.container_info['NetworkSettings']['Ports']['5901/tcp'][0]['HostPort']
            ip = new_container.container_info['NetworkSettings']['IPAddress']

            new_container.host_port = ip + " : " + port

            new_container.save()

            return new_container

        except Exception as e:
            self.logger.debug(e)
            raise e

    def rm_container(self, container_name):
        """
        Remove a container (container_name)
        :param container_name: container name to be removed
        """
        self.logger.debug('Attempting to remove container %s' % container_name)

        try:
            self.client.api.remove_container(container_name)

            container = CalipsoContainer.objects.get(container_name=container_name, container_status='stopped')
            container.container_status = 'removed'
            container.save()

            self.logger.debug('Container ' + container_name + ' has been removed')

            return container

        except Exception as e:
            self.logger.debug(e)
            raise e

    def stop_container(self, container_name):
        """
        Stop a container (container_name)
        :param container_name: container id to be stopped
        :return: none
        """
        self.logger.debug('Attempting to stop a container %s' % container_name)

        try:
            self.client.api.stop(container_name)

            container = CalipsoContainer.objects.get(container_name=container_name, container_status='created')
            container.container_status = 'stopped'
            container.save()

            self.logger.debug('Container ' + container_name + ' has been stopped')
            return container

        except Exception as e:
            self.logger.debug(e)
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
            self.logger.debug(e)
            raise e