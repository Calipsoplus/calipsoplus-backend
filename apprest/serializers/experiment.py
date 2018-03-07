from rest_framework import serializers
from apprest.models.experiments import CalipsoExperiment


class CalipsoExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'subject', 'body')
        model = CalipsoExperiment
