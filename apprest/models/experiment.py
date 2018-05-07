from django.db import models


class CalipsoExperiment(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    serial_number = models.CharField(max_length=50, blank=True)
    beam_line = models.CharField(max_length=200, blank=True)

    def create(self, subject, body, serial_number, beam_line):
        self.subject = subject
        self.body = body
        self.serial_number = serial_number
        self.beam_line = beam_line

    class Meta:
        db_table = 'calipso_experiments'

    def __str__(self):
        return self.subject