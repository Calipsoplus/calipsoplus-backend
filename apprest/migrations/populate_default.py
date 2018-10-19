from django.db import migrations
from apprest.models.image import CalipsoAvailableImages

def create_image_default(apps, schema_editor):
    default_data_image=[
        ('base_image', '', 'consol/centos-xfce-vnc:latest', 1, '3G', '5G'),
        ('base_jupyter', '', 'jupyter/scipy-notebook', 1, '3G', '5G')]

    for image_data in default_data_image:
        public_name = image_data[0]
        docker_daemon = image_data[1]
        image = image_data[2]
        cpu = image_data[3]
        memory = image_data[4]
        hdd = image_data[5]
        try:
            CalipsoAvailableImages.objects.create(public_name=public_name,docker_daemon=docker_daemon,image=image,cpu=cpu,memory=memory,hdd=hdd)
        except Exception as e:
            print('Error creating image_default: %s' % e)


class Migration(migrations.Migration):
    dependencies = [
        ('apprest', '0001_initial'),
    ]
    operations = [migrations.RunPython(create_image_default)]
