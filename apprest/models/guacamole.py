# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class GuacamoleConnection(models.Model):
    connection_id = models.AutoField(primary_key=True)
    connection_name = models.CharField(max_length=128)
    parent = models.ForeignKey('GuacamoleConnectionGroup', models.DO_NOTHING, blank=True, null=True)
    protocol = models.CharField(max_length=32)
    proxy_port = models.IntegerField(blank=True, null=True)
    proxy_hostname = models.CharField(max_length=512, blank=True, null=True)
    proxy_encryption_method = models.CharField(max_length=4, blank=True, null=True)
    max_connections = models.IntegerField(blank=True, null=True)
    max_connections_per_user = models.IntegerField(blank=True, null=True)
    connection_weight = models.IntegerField(blank=True, null=True)
    failover_only = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'guacamole_connection'
        unique_together = (('connection_name', 'parent'),)


class GuacamoleConnectionGroup(models.Model):
    connection_group_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    connection_group_name = models.CharField(max_length=128)
    type = models.CharField(max_length=14)
    max_connections = models.IntegerField(blank=True, null=True)
    max_connections_per_user = models.IntegerField(blank=True, null=True)
    enable_session_affinity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'guacamole_connection_group'
        unique_together = (('connection_group_name', 'parent'),)


class GuacamoleConnectionParameter(models.Model):
    connection = models.ForeignKey(GuacamoleConnection, models.DO_NOTHING, primary_key=False)
    parameter_name = models.CharField(max_length=128)
    parameter_value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'guacamole_connection_parameter'
        unique_together = (('connection', 'parameter_name'),)


class GuacamoleConnectionPermission(models.Model):
    user = models.ForeignKey('GuacamoleUser', models.DO_NOTHING, primary_key=False)
    connection = models.ForeignKey(GuacamoleConnection, models.DO_NOTHING)
    permission = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'guacamole_connection_permission'
        unique_together = (('user', 'connection', 'permission'),)


class GuacamoleUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=128)
    password_hash = models.BinaryField()
    password_salt = models.BinaryField(blank=True, null=True)
    password_date = models.DateTimeField()
    disabled = models.IntegerField()
    expired = models.IntegerField()
    access_window_start = models.TimeField(blank=True, null=True)
    access_window_end = models.TimeField(blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=64, blank=True, null=True)
    full_name = models.CharField(max_length=256, blank=True, null=True)
    email_address = models.CharField(max_length=256, blank=True, null=True)
    organization = models.CharField(max_length=256, blank=True, null=True)
    organizational_role = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guacamole_user'


