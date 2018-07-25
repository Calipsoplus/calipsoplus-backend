from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apprest.models.experiment import CalipsoUserExperiment
from apprest.serializers.users_experiments import CalipsoUserExperimentSerializer


class CalipsoExperimentFavorite(UpdateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoUserExperimentSerializer
    pagination_class = None

    def put(self, request, *args, **kwargs):
        try:
            user_experiment = CalipsoUserExperiment.objects.get(pk=self.kwargs.get('pk'))
        except CalipsoUserExperiment.DoesNotExist:
            raise NotFound

        serializer = CalipsoUserExperimentSerializer(user_experiment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=ValidationError)