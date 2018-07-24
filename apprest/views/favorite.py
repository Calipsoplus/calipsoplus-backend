from django.http import Http404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apprest.models.experiment import CalipsoUserExperiment
from apprest.serializers.users_experiments import CalipsoUserExperimentSerializer


class CalipsoExperimentFavorite(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoUserExperimentSerializer
    pagination_class = None

    def get_object(self, pk):
        try:
            return CalipsoUserExperiment.objects.get(pk=pk)
        except CalipsoUserExperiment.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        user_experiment = self.get_object(pk)
        serializer = CalipsoUserExperimentSerializer(user_experiment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)