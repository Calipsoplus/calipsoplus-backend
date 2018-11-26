from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apprest.serializers.image import CalipsoImageSerializer
from apprest.serializers.quota import CalipsoUserQuotaSerializer
from apprest.services.image import CalipsoAvailableImagesServices


class GetUsedQuotaFromUser(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoUserQuotaSerializer

    pagination_class = None

    def get_queryset(self):
        service = CalipsoAvailableImagesServices()

        username = self.kwargs.get('username')
        if username == self.request.user.username:
            return service.get_sum_containers_quota(username=username)
        else:
            raise PermissionDenied


class GetInfoImage(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoImageSerializer

    pagination_class = None

    def get(self, *args, **kwargs):
        service = CalipsoAvailableImagesServices()
        public_name = self.kwargs.get('public_name')
        image = service.get_available_image(public_name=public_name)
        serializer_class = CalipsoImageSerializer(image)
        return Response(serializer_class.data)
