from django.db import models
from simple_history.models import HistoricalRecords


class CalipsoAvailableImages(models.Model):
    public_name = models.CharField(max_length=255, unique=True)
    docker_daemon = models.CharField(default="", max_length=255)
    image = models.CharField(max_length=255)
    cpu = models.IntegerField()
    memory = models.CharField(max_length=100)
    hdd = models.CharField(max_length=100)

    history = HistoricalRecords()

    class Meta:
        db_table = 'calipso_images'

    def __str__(self):
        return self.public_name

