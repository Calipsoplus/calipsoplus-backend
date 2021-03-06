import logging

from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
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

    logger = logging.getLogger(__name__)

    def put(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            user_experiment = CalipsoUserExperiment.objects.get(pk=pk)
            if user_experiment.calipso_user.user != request.user:
                self.logger.debug("PermissionDenied: calipso_user.user != request.user")
                raise PermissionDenied
        except CalipsoUserExperiment.DoesNotExist:
            raise NotFound

        serializer = CalipsoUserExperimentSerializer(user_experiment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.logger.debug("Favorite (%s) changed correctly" % pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=ValidationError)
