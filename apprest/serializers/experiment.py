from rest_framework import serializers
from apprest.models.experiment import CalipsoExperiment


class CalipsoExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('serial_number', 'subject', 'body', 'beam_line')
        model = CalipsoExperiment

    def to_representation(self, instance):
        data = super(CalipsoExperimentSerializer, self).to_representation(instance)

        data['id'] = instance.calipsouserexperiment_set.get().id
        data['favorite'] = instance.calipsouserexperiment_set.get().favorite

        return data