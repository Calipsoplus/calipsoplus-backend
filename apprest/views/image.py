from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

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


class GetInfoImage(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoUserQuotaSerializer

    pagination_class = None

    def get_queryset(self):
        service = CalipsoAvailableImagesServices()
        public_name = self.kwargs.get('public_name')

        return service.get_available_image(public_name=public_name)


class GetAllImages(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoImageSerializer

    pagination_class = None

    def get_queryset(self):
        service = CalipsoAvailableImagesServices()

        return service.get_all_images()
