from rest_framework import serializers

from apprest.models.experiment import CalipsoUserExperiment


class CalipsoUserExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('calipso_user', 'calipso_experiment', 'favorite')
        model = CalipsoUserExperiment