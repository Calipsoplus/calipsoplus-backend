import logging

from django.db import migrations

from apprest.utils.migrations import create_image_default

logger = logging.getLogger(__name__)


def my_function(apps, schema_editor):
    # logger.debug('apps = %s, schema_editor = %s' % (apps, schema_editor))
    create_image_default()


class Migration(migrations.Migration):
    dependencies = [
        ('apprest', '0003_populate_resources_types'),
    ]
    operations = [migrations.RunPython(my_function)]
