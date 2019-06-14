from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apprest.plugins.icat.helpers.complex_encoder import JsonResponse
from apprest.plugins.icat.services.ICAT import ICATService


class GetInvestigationUsers(APIView):
    """
    get:
    Return: Users involved in an investigation
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    pagination_class = None

    def get(self, *args, **kwargs):
        service = ICATService()
        investigation_id = self.kwargs.get('investigation_id')
        investigation_users = service.get_users_involved_in_investigation(investigation_id)

        return JsonResponse(investigation_users, status=status.HTTP_200_OK)
