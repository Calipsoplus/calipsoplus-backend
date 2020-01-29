import logging
import re
import uuid
import docker

from apprest.models import CalipsoUser
from apprest.models.container import CalipsoContainer
from apprest.services.experiment import CalipsoExperimentsServices
from apprest.services.image import CalipsoAvailableImagesServices

from django.conf import settings

from apprest.services.session import CalipsoSessionsServices
from apprest.utils.exceptions import DockerExceptionNotFound
from apprest.services.user import CalipsoUserServices
from calipsoplus.settings_calipso import ADD_HOME_DIR_TO_ALL_CONTAINERS

image_service = CalipsoAvailableImagesServices()
session_service = CalipsoSessionsServices()
experiments_service = CalipsoExperimentsServices()
user_service = CalipsoUserServices()


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
            self.logger.debug('Docker daemon not found %s' % e)
            raise DockerExceptionNotFound("Docker daemon not found.")

        image_selected = image_service.get_available_image(public_name=public_name)

        uid = "-1"
        gid = "-1"
        try:
            experiment_from_session = session_service.get_experiment_from_session(session_number=experiment)
            experiment_data = experiments_service.get_experiment(proposal_id=experiment_from_session.proposal_id)
            uid = experiment_data.uid
            gid = experiment_data.gid
        except Exception as e:
            self.logger.debug('Exception on get experiments,sessions, and uid,gid')

        # If there was an exception getting the UID and GID from the experiment, try to get it from the user
        if uid == '-1' or gid == '-1':
            try:
                uid = user_service.get_user_uid(username)
                gid = user_service.get_user_gid(username)
                self.logger.debug('Getting UID and GID from user')
                self.logger.debug('uid:%s, gid:%s' % (uid, gid))
            except Exception as e:
                self.logger.error(e)
                self.logger.debug('Getting UID and GID from experiment and user has failed. Setting values to root')
                uid, gid = 0, 0

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

        # Check to add home directory to the container
        if ADD_HOME_DIR_TO_ALL_CONTAINERS:
            volume.update(
                {str(user_service.get_user_home_dir(username)): {"bind": "/tmp/user/home/", "mode": "rw"}}
            )

        self.logger.debug('volume set to :%s', volume)

        self.logger.debug('creating container')
        user = CalipsoUser.objects.get(user__username=username)
        new_container = CalipsoContainer.objects.create(calipso_user=user,
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
        # Group 100 needed for containers supported by Calipso
        groups = settings.GROUPS_DOCKER_ADD + [100]

        try:
            self.logger.debug('client docker run')
            docker_container = self.client.containers.run(image=image_selected.image,
                                                          detach=True,
                                                          publish_all_ports=True,
                                                          mem_limit=image_selected.memory,
                                                          memswap_limit=-1,
                                                          cpu_count=image_selected.cpu,
                                                          environment=["PYTHONUNBUFFERED=0"],
                                                          working_dir="/tmp/results/" + username,
                                                          volumes=volume,
                                                          group_add=groups,
                                                          user="%s:%s" % (uid, gid),
                                                          )
            self.logger.debug('client docker after run')
            new_container.container_id = docker_container.id
            new_container.container_name = docker_container.name
            new_container.container_status = docker_container.status
            new_container.container_info = self.client.api.inspect_container(docker_container.id)
            new_container.image = image_selected
            new_container.num_cpus = image_selected.cpu
            new_container.memory_allocated = image_selected.memory
            new_container.hdd_allocated = image_selected.hdd

            items = new_container.container_info['NetworkSettings']['Ports']

            port = self.get_port_from_container(image_selected, items)

            result_er = ""
            for log in docker_container.logs(stream=True):
                self.logger.debug(str(log))
                result_er = re.findall(image_selected.logs_er, str(log))
                if result_er:
                    break

            new_container.host_port = port

            if result_er[0] != image_selected.logs_er:
                new_container.host_port = "http://" + settings.REMOTE_MACHINE_IP + ":" + str(port) + "/?" + result_er[0]

            new_container.save()

            self.logger.debug('Return a new container, image:%s', image_selected.image)
            return new_container

        except Exception as e:
            # self.logger.error(e)
            new_container.container_status = "error"
            new_container.save()
            raise Exception("Can not run the container. ErrorMsg:%s" % e)

    @staticmethod
    def get_port_from_container(image_selected, items):
        port = 0
        if image_selected.protocol.upper() == 'RDP' and '3389/tcp' in items.keys():
            port = items['3389/tcp'][0]['HostPort']
        elif image_selected.protocol.upper() == 'VNC' and '5901/tcp' in items.keys():
            port = items['5901/tcp'][0]['HostPort']
        elif '8888/tcp' in items.keys():
            port = items['8888/tcp'][0]['HostPort']
        return port

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
            user = CalipsoUser.objects.get(user__username=username)
            containers = CalipsoContainer.objects.filter(calipso_user=user,
                                                         container_status__in=['created', 'busy'])
            self.logger.debug('List containers from ' + username)
            return containers

        except Exception as e:
            self.logger.error("List container error")
            self.logger.error(e)
            raise e
