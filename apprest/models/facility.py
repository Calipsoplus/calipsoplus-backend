from django.db import models
from simple_history.models import HistoricalRecords


class CalipsoFacility(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.CharField(max_length=2083)

    history = HistoricalRecords()


    def create(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    class Meta:
        db_table = 'calipso_facilities'

    def __str__(self):
        return self.name