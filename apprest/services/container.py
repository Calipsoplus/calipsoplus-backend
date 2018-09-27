import logging
import re
import uuid
import docker

from apprest.models.container import CalipsoContainer
from apprest.services.image import CalipsoAvailableImagesServices

from django.conf import settings

from apprest.services.quota import CalipsoUserQuotaServices
from apprest.utils.exceptions import QuotaMaxSimultaneousExceeded, QuotaHddExceeded, QuotaMemoryExceeded, \
    QuotaCpuExceeded

JUPYTER_REGEX_LOGS = 'token=(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
DESKTOP_REGEX_LOGS = 'connect via'

quota_service = CalipsoUserQuotaServices()
image_service = CalipsoAvailableImagesServices()


class CalipsoContainersServices:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.client = docker.DockerClient(tls=False, base_url=settings.DOCKER_URL_DAEMON)
            self.logger.debug('Docker deamon has been initialized')
        except Exception as e:
            self.logger.critical("Docker deamon not found.")
            self.logger.critical(e)

    def run_container(self, username, experiment, container_public_name):
        """
        Run a new container
        returns a container created
        :param username
        :param experiment
        :param container_public_name:
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
            self.logger.debug("container with public_name=%s" % container.public_name)

        try:
            quota_per_user = quota_service.get_default_quota(username=username)[0]
        except Exception as e:
            self.logger.error("Problem to get quota from %s user" % username)
            self.logger.error(e)

        self.logger.debug("num_containers_per_user = %d" % len(list_of_containers))

        if max_simultaneous >= quota_per_user.max_simultaneous:
            self.logger.warning(
                'user:%s used:%d > quota.max:%d' % (username, max_simultaneous, quota_per_user.max_simultaneous))
            raise QuotaMaxSimultaneousExceeded("Max machines exceeded")

        if max_cpu >= quota_per_user.cpu:
            self.logger.warning('user:%s cpu_used:%d > quota.max_cpu:%d' % (username, max_cpu, quota_per_user.cpu))
            raise QuotaCpuExceeded("Max cpus exceeded")

        if max_memory >= int(quota_per_user.memory[:-1]):
            self.logger.warning(
                'user:%s max_ram_used:%dG > quota_user.max_ram:%s' % (username, max_memory, quota_per_user.memory))
            raise QuotaMemoryExceeded("Max memory exceeded")

        if max_hdd >= int(quota_per_user.hdd[:-1]):
            self.logger.warning('user:%s max_hdd:%dG quota.max_hdd:%s' % (username, max_hdd, quota_per_user.hdd))
            raise QuotaHddExceeded("Max hdd exceeded")

        image_selected = image_service.get_available_image(public_name=container_public_name)[0]

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
                                                          cpu_count=image_selected.cpu,
                                                          environment=["PYTHONUNBUFFERED=0"]
                                                          )
            new_container.container_id = docker_container.id
            new_container.container_name = docker_container.name
            new_container.container_status = docker_container.status
            new_container.container_info = self.client.api.inspect_container(docker_container.id)

            for key, val in new_container.container_info['NetworkSettings']['Ports'].items():
                port = int(val[0]['HostPort'])
                break

            result_jupyter = ""
            for log in docker_container.logs(stream=True):
                result_jupyter = re.findall(JUPYTER_REGEX_LOGS, str(log))
                result_desktop = re.findall(DESKTOP_REGEX_LOGS, str(log))
                if result_jupyter or result_desktop:
                    break

            if result_jupyter:
                new_container.host_port = "http://" + settings.REMOTE_MACHINE_IP + ":" + str(port) + "/?" + result_jupyter[0]

            new_container.save()

            self.logger.debug('Return a new container, image:%s', image_selected.image)
            return new_container

        except Exception as e:
            self.logger.error("Run container error")
            self.logger.error(e)
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
            self.logger.error("Remove container error")
            self.logger.error(e)
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
            self.logger.error("Stop container error")
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