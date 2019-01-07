from django.db import models
from simple_history.models import HistoricalRecords

from apprest.models.user import CalipsoUser
from calipsoplus.settings_calipso import MAX_CONTAINER_PER_USER, MAX_STORAGE_PER_USER, MAX_RAM_PER_USER, \
    MAX_CPU_PER_USER


class CalipsoUserQuota(models.Model):
    calipso_user = models.OneToOneField(CalipsoUser, on_delete=models.CASCADE, blank=True)
    max_simultaneous = models.IntegerField(default=MAX_CONTAINER_PER_USER)
    cpu = models.IntegerField(default=MAX_CPU_PER_USER)
    memory = models.CharField(default=MAX_RAM_PER_USER, max_length=100)
    hdd = models.CharField(default=MAX_STORAGE_PER_USER, max_length=100)

    history = HistoricalRecords()

    class Meta:
        db_table = 'calipso_quotas'

    def __str__(self):
        return str(self.cpu) + "_" + str(
            self.max_simultaneous) + "_" + str(self.memory) + "_" + str(self.hdd)


