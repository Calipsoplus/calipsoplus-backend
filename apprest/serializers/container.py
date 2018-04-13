from rest_framework import serializers
from apprest.models.container import CalipsoContainer


class CalipsoContainerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('uid', 'container','status','ip')
        model = CalipsoContainer
