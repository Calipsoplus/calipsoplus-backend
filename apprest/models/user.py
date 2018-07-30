import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from simple_history.models import HistoricalRecords


class CalipsoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    calipso_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    history = HistoricalRecords()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            CalipsoUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        db_table = 'calipso_users'

    def __str__(self):
        return str(self.calipso_uid)

