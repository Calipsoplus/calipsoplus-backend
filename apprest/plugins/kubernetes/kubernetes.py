# import string
# import random
#
# from kubernetes import client, config, utils
#
#
# def id_generator(size=12, chars=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))
#
#
# def create_deployment_object(username, deployment_name, container_image, label_selector, uid=0, gid=0):
#     # Configure Pod template container
#     deployment_name = str(deployment_name)
#     username = str(username)
#
#     container = create_container(username, container_image, uid=uid, gid=gid)
#
#     # Create the volumes
#     # Volumes are directories that are on the host (machine running the containers)
#     volumes = [
#         client.V1Volume(name='tmp',
#                         host_path=client.V1HostPathVolumeSource(path='/tmp', type='Directory'))
#     ]
#
#     pod_security_context = client.V1PodSecurityContext(run_as_user=uid, run_as_group=gid, run_as_non_root=True,
#                                                        supplemental_groups=[100])
#     # Create and configurate a spec section
#     template = client.V1PodTemplateSpec(
#         metadata=client.V1ObjectMeta(labels={"app": label_selector}),
#         spec=client.V1PodSpec(containers=[container], volumes=volumes, security_context=pod_security_context))
#     # Create the specification of deployment
#     spec = client.ExtensionsV1beta1DeploymentSpec(
#         replicas=1,
#         template=template,
#         selector=client.V1LabelSelector(
#             match_labels={"app": label_selector})
#     )
#     # Instantiate the deployment object
#     deployment = client.ExtensionsV1beta1Deployment(
#         api_version="extensions/v1beta1",
#         kind="Deployment",
#         metadata=client.V1ObjectMeta(name=deployment_name + id_generator()),
#         spec=spec)
#
#     return deployment
#
#
# def create_deployment(api_instance, deployment, namespace):
#     # Create deployment
#     api_response = api_instance.create_namespaced_deployment(
#         body=deployment,
#         namespace=str(namespace))
#     print("Deployment created. status='%s'" % str(api_response.status))
#
#
# def create_container(username, container_image, cpu=1, memory='2Gi', uid=0, gid=0):
#     container_name = '%s-%s' % (username, str(id_generator()))
#     container_image = str(container_image)
#
#     # Create the security contexts
#     # These will determine which user is running the container and the groups they belong to
#     security_context = client.V1SecurityContext(run_as_user=uid, run_as_group=gid, run_as_non_root=True)
#
#     # Mount the volumes to the container
#     # mountpath is the path the volume will be mounted to in the container
#     # The name must be the same as one of the volumes previously created
#     volume_mounts = [
#         client.V1VolumeMount(mount_path='/tmp', name='tmp'),
#     ]
#
#     # Set the hardware requirements for the container
#     # Requests are the minimum hardware requirements
#     # Limits are the maximum hardware requirements
#     # Always requests <= limits
#     resources = client.V1ResourceRequirements(requests={'cpu': str(cpu), 'memory': memory})
#     container = client.V1Container(
#         name=container_name, image=container_image, resources=resources,
#         security_context=security_context, volume_mounts=volume_mounts,
#         ports=[
#             client.V1ContainerPort(container_port=3389),
#             client.V1ContainerPort(container_port=5901),
#             client.V1ContainerPort(container_port=8888)
#         ])
#     return container
#
#
# def create_service(selector_label, ports, namespace):
#     config.load_kube_config()
#     api_instance = client.CoreV1Api()
#
#     service = client.V1Service()
#
#     service.api_version = "v1"
#     service.kind = "Service"
#     service.metadata = client.V1ObjectMeta(name="%s-service" % selector_label)
#
#     spec = client.V1ServiceSpec()
#     spec.selector = {"app": selector_label}
#     spec.ports = []
#     for key in ports:
#         spec.ports.append(client.V1ServicePort(protocol="TCP", name=key, port=ports[key], target_port=ports[key]))
#     spec.type = 'NodePort'
#     service.spec = spec
#
#     api_response = api_instance.create_namespaced_service(namespace=namespace, body=service)
#     print("Service created. status='%s'" % str(api_response.status))
#
#
# def create_deployment_and_service(deployment_name, container_image, username, namespace='default'):
#     config.load_kube_config()
#
#     label_selector = "%s-%s-%s" % (deployment_name, username, str(id_generator()))
#     deployment = create_deployment_object(username, deployment_name, container_image, label_selector, 1111111, 20000)
#
#     create_deployment(client.ExtensionsV1beta1Api(), deployment, namespace)
#     create_service(label_selector, {'rdp': 3389, 'vnc': 5901, 'something': 8888}, namespace)
#
#
# if __name__ == "__main__":
#     create_deployment_and_service('rdp', 'aicampbell/vnc-ubuntu18-xfce', 'user')
