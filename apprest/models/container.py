from django.db import models

from apprest.models.experiments import CalipsoExperiment
from apprest.models.user import CalipsoUser

class CalipsoContainer(models.Model):

    container = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    ip = models.CharField(max_length=15)

    calipso_user = models.ForeignKey(CalipsoUser, on_delete=models.CASCADE, null=False)
    calipso_experiment = models.ForeignKey(CalipsoExperiment, on_delete=models.CASCADE, null=False)


    class Meta:
        db_table = 'calipso_containers'
        unique_together = ("calipso_user", "calipso_experiment")

    def __str__(self):
        return self.container