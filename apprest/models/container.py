from django.db import models


class CalipsoContainer(models.Model):
    calipso_user = models.CharField(max_length=255)
    calipso_experiment = models.CharField(max_length=255)
    container_id = models.CharField(max_length=255)
    container_name = models.CharField(max_length=255)
    container_status = models.CharField(max_length=25)
    container_info = models.TextField()
    container_logs = models.TextField()

    class Meta:
        db_table = 'calipso_containers'
        # unique_together = (('calipso_user', 'calipso_experiment'),)

    def __str__(self):
        return self.container_name
