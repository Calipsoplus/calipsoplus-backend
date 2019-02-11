import django
from django.db import models
from simple_history.models import HistoricalRecords


class CalipsoResourcesType(models.Model):
    resource_type = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'calipso_resource_types'


class CalipsoAvailableImages(models.Model):
    public_name = models.CharField(max_length=255, unique=True)
    image = models.CharField(max_length=255)
    docker_daemon = models.CharField(default="", max_length=255)
    host_domain = models.CharField(default="", max_length=255)
    port_hook = models.CharField(max_length=255)
    logs_er = models.CharField(max_length=255)
    protocol = models.CharField(max_length=25)
    cpu = models.IntegerField()
    memory = models.CharField(max_length=100)
    hdd = models.CharField(max_length=100)

    resource_type = models.ForeignKey(CalipsoResourcesType, on_delete=django.db.models.deletion.CASCADE, blank=True,
                                      null=True)


    #label
    #icon

    history = HistoricalRecords()

    class Meta:
        db_table = 'calipso_images'

    def __str__(self):
        return self.public_name
