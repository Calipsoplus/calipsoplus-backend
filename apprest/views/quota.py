from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from apprest.serializers.quota import CalipsoUserQuotaSerializer
from apprest.services.quota import CalipsoUserQuotaServices


class QuotaView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get(self, request, username):
        service = CalipsoUserQuotaServices()
        username = self.kwargs.get('username')
        if username == self.request.user.username:
            quote = service.get_default_quota(username=username)
            serializer_class = CalipsoUserQuotaSerializer(quote, many=True)
            return Response(serializer_class.data)
        else:
            raise PermissionDenied

    def post(self, request, username):
        data = request.data
        service = CalipsoUserQuotaServices()
        username = self.kwargs.get('username')
        # Todo add check to make sure current logged in user is an admin
        service.change_user_quota(username=username, max_simulations=data['max_simultaneous'],
                                      memory=data['memory'], cpu=data['cpu'], hdd=data['hdd'])
        return Response(status=status.HTTP_200_OK)

