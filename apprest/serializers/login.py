
from rest_framework import serializers


class LoginCustomSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=200)
  password = serializers.CharField(max_length=200)