from django.db import models
from simple_history.models import HistoricalRecords


class CalipsoQuotas(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    cpus = models.IntegerField()
    memory = models.CharField(max_length=100)
    hdd = models.CharField(max_length=100)
    type = models.CharFiled(default='docker', max_lenght=100)

    history = HistoricalRecords()

    def create(self, name, image, cpus, memory, hdd, type):
        self.name = name
        self.image = image
        self.cpus = cpus
        self.memory = memory
        self.hdd = hdd
        self.type = type

    class Meta:
        db_table = 'calipso_quotas'

    def __str__(self):
        return self.name