from rest_framework import serializers
from apprest.models.quota import CalipsoUserQuota


class CalipsoUserQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('cpu', 'memory', 'hdd', 'max_simultaneous')
        model = CalipsoUserQuota

