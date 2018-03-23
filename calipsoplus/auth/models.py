from django.db import models
from django.contrib.auth.models import User

class AuthDatabaseUser(models.Model):
    login = models.CharField(db_column='Login')
    password = models.CharField(db_column='Password')

    def __str__(self):
        return self.login

    class Meta:
        managed = False
        db_table = 'User'
        app_label = 'auth'
