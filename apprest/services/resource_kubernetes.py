import logging
import random
import string
import uuid
import os

from kubernetes import client, config

from apprest.models.container import CalipsoContainer
from apprest.services.experiment import CalipsoExperimentsServices
from apprest.services.image import CalipsoAvailableImagesServices
from apprest.services.session import CalipsoSessionsServices
from apprest.services.user import CalipsoUserServices
from calipsoplus.settings_calipso import ADD_HOME_DIR_TO_ALL_CONTAINERS, EXPERIMENTS_DATASETS_ROOT, EXPERIMENTS_OUTPUT

image_service = CalipsoAvailableImagesServices()
session_service = CalipsoSessionsServices()
experiments_service = CalipsoExperimentsServices()
user_service = CalipsoUserServices()


class CalipsoResourceKubernetesService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('CalipsoResourceKubernetesService initialized')

        try:
            # Assumes that the kubernetes config file is in the home directory. This could be configurable later
            config.load_kube_config(os.path.join(os.environ["HOME"], '.kube/config'))
        except FileNotFoundError as e:
            self.logger.error(e)
            self.logger.error('Kubernetes configuration file does not exist')
        except Exception as e:
            self.logger.error(e)

    def id_generator(self, size=12, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_pod_full_name(self, pod_name, namespace='default'):
        api_instance = client.CoreV1Api()

        results = api_instance.list_namespaced_pod(namespace=namespace)
        for i in results.items:
            if pod_name in i.metadata.name:
                return i.metadata.name

        self.logger.debug('Pod %s does not exist' % pod_name)
        return Exception

    def get_pod_status(self, pod_full_name, namespace='default'):
        api_instance = client.CoreV1Api()

        api_response = api_instance.read_namespaced_pod_status(pod_full_name, namespace)
        return api_response.status.phase

    def create_deployment_object(self, username, deployment_name, container_image, label_selector, uid=0, gid=0):
        # Configureate Pod template container
        deployment_name = str(deployment_name)
        username = str(username)

        container = self.create_container(username, container_image, uid=uid, gid=gid)

        # Create the volumes
        # Volumes are directories that are on the host (machine running the containers)
        volumes = [
            client.V1Volume(name='tmp-data',
                            host_path=client.V1HostPathVolumeSource(path=EXPERIMENTS_DATASETS_ROOT, type='Directory')),
            client.V1Volume(name='tmp-results',
                            host_path=client.V1HostPathVolumeSource(path=EXPERIMENTS_OUTPUT, type='Directory')),
        ]

        if ADD_HOME_DIR_TO_ALL_CONTAINERS:
            volumes.append(client.V1Volume(name='user-home',
                                           host_path=client.V1HostPathVolumeSource(
                                               path=user_service.get_user_home_dir(username),
                                               type='Directory')))

        pod_security_context = client.V1PodSecurityContext(run_as_user=uid, run_as_group=gid, supplemental_groups=[100])
        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": label_selector}),
            # spec=client.V1PodSpec(containers=[container], volumes=volumes, security_context=pod_security_context))
            spec=client.V1PodSpec(containers=[container], security_context=pod_security_context))
        # Create the specification of deployment
        spec = client.ExtensionsV1beta1DeploymentSpec(
            replicas=1,
            template=template,
            selector=client.V1LabelSelector(
                match_labels={"app": label_selector})
        )
        # Instantiate the deployment object
        deployment = client.ExtensionsV1beta1Deployment(
            api_version="extensions/v1beta1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name),
            spec=spec)

        return deployment

    def create_deployment(self, api_instance, deployment, namespace):
        # Create deployment
        api_response = api_instance.create_namespaced_deployment(
            body=deployment,
            namespace=str(namespace))
        print("Deployment created. status='%s'" % str(api_response.status))

    def create_container(self, username, container_image, cpu='0.5', memory='0.5Gi', uid=0, gid=0):
        container_name = '%s-%s' % (username, str(self.id_generator()))
        container_image = str(container_image)

        # Create the security contexts
        # These will determine which user is running the container and the groups they belong to
        security_context = client.V1SecurityContext(run_as_user=uid, run_as_group=gid)

        # Mount the volumes to the container
        # mountpath is the path the volume will be mounted to in the container
        # The name must be the same as one of the volumes previously created
        volume_mounts = [
            client.V1VolumeMount(mount_path=EXPERIMENTS_DATASETS_ROOT, name='tmp-data'),
            client.V1VolumeMount(mount_path=EXPERIMENTS_OUTPUT, name='tmp-results')
        ]

        # Check if user home directory should be mounted to container
        if ADD_HOME_DIR_TO_ALL_CONTAINERS:
            volume_mounts.append(client.V1VolumeMount(mount_path=user_service.get_user_home_dir(username=username),
                                                      name='user-home'))

        # Set the hardware requirements for the container
        # Requests are the minimum hardware requirements
        # Limits are the maximum hardware requirements
        # Always requests <= limits
        resources = client.V1ResourceRequirements(requests={'cpu': str(cpu), 'memory': memory})
        container = client.V1Container(
            name=container_name, image=container_image, resources=resources,
            # security_context=security_context, volume_mounts=volume_mounts,
            security_context=security_context,
            ports=[
                client.V1ContainerPort(container_port=3389),
                client.V1ContainerPort(container_port=5901),
                client.V1ContainerPort(container_port=8888)
            ])
        return container

    def create_service(self, selector_label, ports, namespace):
        api_instance = client.CoreV1Api()
        service = client.V1Service()

        service.api_version = "v1"
        service.kind = "Service"
        service.metadata = client.V1ObjectMeta(name="%s-service" % selector_label)

        spec = client.V1ServiceSpec()
        spec.selector = {"app": selector_label}
        spec.ports = []
        for key in ports:
            spec.ports.append(
                client.V1ServicePort(protocol="TCP", name=key, port=ports[key], target_port=ports[key]))
        spec.type = 'NodePort'
        service.spec = spec

        api_response = api_instance.create_namespaced_service(namespace=namespace, body=service)
        print("Service created. status='%s'" % str(api_response.status))

    def create_deployment_and_service(self, deployment_name, container_image, username, namespace='default',
                                      uid=0, gid=0):
        label_selector = deployment_name
        deployment = self.create_deployment_object(username, deployment_name, container_image, label_selector, uid, gid)

        self.create_deployment(client.ExtensionsV1beta1Api(), deployment, namespace)
        self.create_service(label_selector, {'rdp': 3389, 'vnc': 5901, 'something': 8888}, namespace)

    def get_ports_from_service(self, deployment_name, namespace='default'):
        api_instance = client.CoreV1Api()
        deployment_name += '-service'
        api_response = api_instance.read_namespaced_service(deployment_name, namespace)

        return api_response.spec.ports

    def get_port_for_container(self, image_selected, items):
        self.logger.debug("Getting ports for container")
        port = 0
        for item in items:
            if image_selected.protocol.upper() == 'RDP' and 3389 == item.port:
                port = item.node_port
                break
            elif image_selected.protocol.upper() == 'VNC' and 5901 == item.port:
                port = item.node_port
                self.logger.debug('vnc and port %s' % port)
                break
            elif 8888 == item.port:
                port = item.node_port
            if port > 0:
                break
        self.logger.debug("Finished Getting ports for container")
        return port

    def delete_deployment(self, deployment_name):
        # Delete deployment
        api_instance = client.AppsV1Api()
        api_response = api_instance.delete_namespaced_deployment(
            name=str(deployment_name),
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))

        self.logger.debug("Deployment deleted. status='%s'" % str(api_response.status))

    def delete_service(self, service_name, namespace='default'):
        # Delete Service
        api_instance = client.CoreV1Api()
        api_response = api_instance.delete_namespaced_service(
            name=str(service_name),
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))

        self.logger.debug("Service deleted. status='%s'" % str(api_response.status))

    def run_resource(self, username, experiment, public_name):
        image_selected = image_service.get_available_image(public_name=public_name)

        uid = "-1"
        gid = "-1"
        try:
            experiment_from_session = session_service.get_experiment_from_session(session_number=experiment)
            experiment_data = experiments_service.get_experiment(proposal_id=experiment_from_session.proposal_id)
            uid = experiment_data.uid
            gid = experiment_data.gid
        except Exception:
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

        deployment_name = username + '-' + self.id_generator()
        self.logger.debug('Creating kubernetes deployment and service for deployment name: %s' % deployment_name)
        self.create_deployment_and_service(deployment_name, image_selected.image, username, uid=uid, gid=gid)

        # generate random values for guacamole credentials
        guacamole_username = uuid.uuid4().hex
        guacamole_password = uuid.uuid4().hex

        vnc_password = 'vncpassword'

        self.logger.debug('creating container')
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

        self.logger.debug('CalipsoResourceKubernetesService run_resource')

        new_container.container_id = uuid.uuid4().hex
        new_container.container_name = self.get_pod_full_name(deployment_name)
        new_container.container_status = "Running"
        new_container.image = image_selected
        new_container.num_cpus = image_selected.cpu
        new_container.memory_allocated = image_selected.memory
        new_container.hdd_allocated = image_selected.hdd

        items = self.get_ports_from_service(deployment_name)
        port = self.get_port_for_container(image_selected, items)

        new_container.host_port = port

        new_container.save()

        return new_container

    def rm_resource(self, resource_name):
        """
        Remove a container (resource_name)
        :param resource_name: container name to be removed
        """
        self.logger.debug('CalipsoResourceKubernetesContainerService rm_resource (%s)' % resource_name)

        try:
            # Kubernetes assigns a longer name to the pod so the first two part of the pod need to be parsed
            # Default format is <username>-<deployment>-<random_string>-<random_string>
            username = resource_name.split('-')[0]
            deployment = resource_name.split('-')[1]
            kube_deployment = '%s-%s' % (username, deployment)
            self.delete_deployment(kube_deployment)
            self.delete_service(kube_deployment + '-service')

            container = CalipsoContainer.objects.get(container_name=resource_name, container_status='stopped')
            container.container_status = 'removed'
            container.save()
        except Exception as e:
            self.logger.error(e)
        self.logger.debug('Container ' + resource_name + ' has been removed')

    def stop_resource(self, resource_name):
        """
        Stop a container (resource_name)
        :param resource_name: container name to be removed

        Kubernetes pods cannot be paused and therefore will be removed instead of stopped
        """
        self.logger.debug('CalipsoResourceKubernetesContainerService stop_resource (%s)' % resource_name)

        try:
            container = CalipsoContainer.objects.get(container_name=resource_name, container_status='Running')
            container.container_status = 'stopped'
            container.save()

            self.logger.debug('Container ' + resource_name + ' has been stopped')

            # Removed the container marked in the DB as stopped
            self.rm_resource(resource_name)
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
        self.logger.debug('CalipsoResourceKubernetesContainerService list_resources (%s)' % username)

        try:
            containers = CalipsoContainer.objects.filter(calipso_user=username,
                                                         container_status__in=['created', 'busy', 'Running'])
            self.logger.debug('List containers from ' + username)
            return containers

        except Exception as e:
            self.logger.error("List container error")
            self.logger.error(e)
            raise e
