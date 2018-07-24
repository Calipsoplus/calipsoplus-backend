from django.db import models
from simple_history.models import HistoricalRecords

from apprest.models.user import CalipsoUser


class CalipsoExperiment(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    serial_number = models.CharField(max_length=50, blank=True)
    beam_line = models.CharField(max_length=200, blank=True)

    calipso_users = models.ManyToManyField(CalipsoUser, through='CalipsoUserExperiment',
                                           through_fields=('calipso_experiment', 'calipso_user'))

    history = HistoricalRecords()

    def create(self, subject, body, serial_number, beam_line):
        self.subject = subject
        self.body = body
        self.serial_number = serial_number
        self.beam_line = beam_line

    class Meta:
        db_table = 'calipso_experiments'

    def __str__(self):
        return self.serial_number


class CalipsoUserExperiment(models.Model):
    calipso_user = models.ForeignKey(CalipsoUser, on_delete=models.CASCADE)
    calipso_experiment = models.ForeignKey(CalipsoExperiment, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False, )

    history = HistoricalRecords()

    class Meta:
        unique_together = ('calipso_user', 'calipso_experiment')
        db_table = 'calipso_user_experiment'

    def __str__(self):
        return str(self.calipso_user) + "-" + str(self.calipso_experiment)