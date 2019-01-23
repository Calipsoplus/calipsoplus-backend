from rest_framework import serializers
from apprest.models.experiment import CalipsoExperiment
from apprest.models.user import CalipsoUser
from apprest.serializers.session import CalipsoSessionSerializer


class CalipsoExperimentSerializer(serializers.ModelSerializer):

    sessions = CalipsoSessionSerializer(many=True)

    class Meta:
        fields = ('proposal_id', 'subject', 'body', 'beam_line', 'sessions')
        model = CalipsoExperiment

    def to_representation(self, instance):
        data = super(CalipsoExperimentSerializer, self).to_representation(instance)

        user = self.context['request'].user
        calipso_user = CalipsoUser.objects.get(user=user)

        data['id'] = instance.calipsouserexperiment_set.get(calipso_user=calipso_user).id
        data['favorite'] = instance.calipsouserexperiment_set.get(calipso_user=calipso_user).favorite

        return data