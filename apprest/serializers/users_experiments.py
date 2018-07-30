from rest_framework import serializers

from apprest.models.experiment import CalipsoUserExperiment


class CalipsoUserExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'favorite')
        model = CalipsoUserExperiment