from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apprest.serializers.user import CalipsoUserSerializer
from apprest.services.user import CalipsoUserServices


class CalipsoUserView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get(self, request):
        service = CalipsoUserServices()
        #TODO: Add requirement for requester to be admin
        users = service.get_all_users(request)

        serializer_class = CalipsoUserSerializer(users, many=True)
        return Response(serializer_class.data)
