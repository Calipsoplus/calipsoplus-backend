from rest_framework import serializers

from apprest.models.user import CalipsoUser


class CalipsoUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'calipso_uid', 'user_id')
        model = CalipsoUser
