from rest_framework import serializers
from apprest.models.facility import CalipsoFacility


class CalipsoFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'description', 'url')
        model = CalipsoFacility
