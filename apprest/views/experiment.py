from django.views.decorators.csrf import csrf_exempt

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
        return service.get_user_experiments(self.kwargs.get('username'))

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(GetExperimentsByUserName, self).dispatch(*args, **kwargs)
