from rest_framework import serializers

from apprest.models.container import CalipsoContainer


class CalipsoContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalipsoContainer

        fields = (
            'calipso_user', 'calipso_experiment', 'container_id', 'container_name', 'container_status',
            'container_logs', 'guacamole_username', 'guacamole_password', 'creation_date', 'host_port', 'public_name',
            'container_info', 'image', 'num_cpus', 'memory_allocated', 'hdd_allocated')