from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apprest.serializers.quota import CalipsoUserQuotaSerializer
from apprest.services.quota import CalipsoUserQuotaServices


class GetDefaultUserQuotasFromUser(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoUserQuotaSerializer
    pagination_class = None

    def get_queryset(self):
        service = CalipsoUserQuotaServices()

        username = self.kwargs.get('username')
        if username == self.request.user.username:
            return service.get_default_quota(username=username)
        else:
            raise PermissionDenied

