from django.db import models
from simple_history.models import HistoricalRecords

from apprest.models import CalipsoExperiment


class CalipsoSession(models.Model):
    session_number = models.CharField(max_length=50, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    data_set_path = models.CharField(max_length=255)
    experiment = models.ForeignKey(CalipsoExperiment, on_delete=models.CASCADE, related_name='sessions')

    history = HistoricalRecords()

    class Meta:
        db_table = 'calipso_sessions'

    def __str__(self):
        return self.session_number