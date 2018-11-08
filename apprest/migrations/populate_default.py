from django.db import migrations
from apprest.models.image import CalipsoAvailableImages


def create_image_default(apps, schema_editor):
    default_data_image = [
        ('base_image',
         'consol/centos-xfce-vnc:latest',
         'tcp://calipsotest.cells.es:2375',
         '192.168.33.13',
         '3389/tcp',
         'connect via',
         'vnc',
         1,
         '3G',
         '5G',
         ),
        ('base_jupyter',
         'jupyter/scipy-notebook',
         'tcp://192.168.33.13:2375',
         '192.168.33.13',
         '3389/tcp',
         'token=(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
         'vnc',
         1,
         '3G',
         '5G',
         ),
        ('base_image_ubuntu',
         'danielguerra/ubuntu-xrdp',
         'tcp://192.168.33.13:2375',
         '192.168.33.13',
         '3389/tcp',
         'startsecs',
         'rdp',
         1,
         '3G',
         '5G',
         )]

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
            CalipsoAvailableImages.objects.create(public_name=public_name, image=image, docker_daemon=docker_daemon,
                                                  host_domain=host_domain, port_hook=port_hook, logs_er=logs_er,
                                                  protocol=protocol, cpu=cpu, memory=memory, hdd=hdd)
        except Exception as e:
            print('Error creating image_default: %s' % e)


class Migration(migrations.Migration):
    dependencies = [
        ('apprest', '0001_initial'),
    ]
    operations = [migrations.RunPython(create_image_default)]
