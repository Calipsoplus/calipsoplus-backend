from rest_framework import serializers

from apprest.models.user import CalipsoUser
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'last_login')
        model = User


class CalipsoUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        fields = ('id', 'calipso_uid', 'user_id', 'user')
        model = CalipsoUser
