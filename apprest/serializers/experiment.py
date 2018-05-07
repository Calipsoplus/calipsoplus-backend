from rest_framework import serializers
from apprest.models.experiment import CalipsoExperiment


class CalipsoExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'subject', 'body')
        model = CalipsoExperiment
