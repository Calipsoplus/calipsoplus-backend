import logging

from apprest.models.image import CalipsoResourcesType, CalipsoAvailableImages

logger = logging.getLogger(__name__)


def create_image_default():
    default_data_image = [
        ("base_image", "consol/centos-xfce-vnc:latest", "tcp://:2375", "", "5901/tcp", "connect via",
         "vnc", 1, "3G", "5G",),
        ("base_jupyter", "jupyter/scipy-notebook:latest", "tcp://:2375", "", "3389/tcp",
         "token=(?:[-\w.]|(?:%[\da-fA-F]{2}))+", "vnc", 1, "3G", "5G",),
        ("base_image_ubuntu", "danielguerra/ubuntu-xrdp:latest", "tcp://:2375", "", "3389/tcp", "startsecs",
         "rdp", 1, "3G", "5G",)]

    resource_type = CalipsoResourcesType.objects.get(resource_type='docker_container')

    for image_data in default_data_image:
        public_name = image_data[0]
        image = image_data[1]
        docker_daemon = image_data[2]
        host_domain = image_data[3]
        port_hook = image_data[4]
        logs_er = image_data[5]
        protocol = image_data[6]
        cpu = image_data[7]
        memory = image_data[8]
        hdd = image_data[9]

        try:
            image_object = CalipsoAvailableImages.objects.get(public_name=public_name)
            image_object.image = image
            image_object.docker_daemon = docker_daemon
            image_object.host_domain = host_domain
            image_object.port_hook = port_hook
            image_object.logs_er = logs_er
            image_object.protocol = protocol
            image_object.cpu = cpu
            image_object.memory = memory
            image_object.hdd = hdd
            image_object.resource_type = resource_type

            image_object.save()

        except Exception as e:
            CalipsoAvailableImages.objects.create(public_name=public_name, image=image, docker_daemon=docker_daemon,
                                                  host_domain=host_domain, port_hook=port_hook, logs_er=logs_er,
                                                  protocol=protocol, cpu=cpu, memory=memory, hdd=hdd,
                                                  resource_type=resource_type)
        except Exception as e:
            logger.error('Error creating image_default: %s' % e)


def create_resources_types():
    resources = ('docker_container', 'kubernetes', 'virtual_machine', 'static_link')
    for resource_type in resources:
        try:
            CalipsoResourcesType.objects.get(resource_type=resource_type)
        except Exception as e:
            try:
                CalipsoResourcesType.objects.create(resource_type=resource_type)
            except Exception as e:
                logger.error('Error creating resources_type: %s' % e)


def create_static_link():
    default_data_image = [
        ("link_google", "https://www.google.com", "", "", "", "",
         "", 1, "3G", "5G",)]

    resource_type = CalipsoResourcesType.objects.get(resource_type='static_link')

    for image_data in default_data_image:
        public_name = image_data[0]
        image = image_data[1]
        docker_daemon = image_data[2]
        host_domain = image_data[3]
        port_hook = image_data[4]
        logs_er = image_data[5]
        protocol = image_data[6]
        cpu = image_data[7]
        memory = image_data[8]
        hdd = image_data[9]

        try:
            image_object = CalipsoAvailableImages.objects.get(public_name=public_name)
            image_object.image = image
            image_object.docker_daemon = docker_daemon
            image_object.host_domain = host_domain
            image_object.port_hook = port_hook
            image_object.logs_er = logs_er
            image_object.protocol = protocol
            image_object.cpu = cpu
            image_object.memory = memory
            image_object.hdd = hdd
            image_object.resource_type = resource_type

            image_object.save()

        except Exception as e:
            CalipsoAvailableImages.objects.create(public_name=public_name, image=image, docker_daemon=docker_daemon,
                                                  host_domain=host_domain, port_hook=port_hook, logs_er=logs_er,
                                                  protocol=protocol, cpu=cpu, memory=memory, hdd=hdd,
                                                  resource_type=resource_type)
        except Exception as e:
            logger.error('Error creating create_static_link: %s' % e)
