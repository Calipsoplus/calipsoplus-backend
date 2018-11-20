from rest_framework import serializers
from apprest.models import CalipsoSession


class CalipsoSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalipsoSession
        fields = ('session_number','start_date','end_date','subject','body','data_set_path')
