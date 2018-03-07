from django.db import models


class CalipsoExperiment(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def create(self, subject, body):
        self.subject = subject
        self.body = body

    class Meta:
        db_table = 'calipso_experiments'

    def __str__(self):
        return self.subject