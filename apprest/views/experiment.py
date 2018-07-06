from rest_framework.exceptions import PermissionDenied

from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from apprest.serializers.experiment import CalipsoExperimentSerializer
from apprest.services.experiment import CalipsoExperimentsServices

service = CalipsoExperimentsServices()


class GetExperimentsByUserName(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoExperimentSerializer
    pagination_class = None

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username == self.request.user.username:
            return service.get_user_experiments(self.kwargs.get('username'))
        else:
            raise PermissionDenied

