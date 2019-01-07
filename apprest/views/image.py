from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status


from apprest.serializers.image import CalipsoImageSerializer
from apprest.serializers.quota import CalipsoUserQuotaSerializer
from apprest.services.image import CalipsoAvailableImagesServices


class GetUsedQuotaFromUser(APIView):
    """
    get:
    Return the used quota for given user
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    pagination_class = None

    def get(self, *args, **kwargs):
        service = CalipsoAvailableImagesServices()
        username = self.kwargs.get('username')
        if username == self.request.user.username:
            quota = service.get_sum_containers_quota(username=username)
            serializer_class = CalipsoUserQuotaSerializer(quota)
            return Response(serializer_class.data)
        else:
            raise PermissionDenied

class GetInfoImage(APIView):
    """
    get:
    Return the given image

    post:
    Add a new image instance

    put:
    Modify an existing image instance

    delete:
    Delete the given image
    """

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

    def post(self, request, *args, **kwargs):
        service = CalipsoAvailableImagesServices()
        public_name = self.kwargs.get('public_name')
        service.add_new_image(public_name=public_name, image=request.data.get('image'),
                             port_hook=request.data.get('port_hook'), logs_er=request.data.get('logs_er'),
                             protocol=request.data.get('protocol'), cpu=request.data.get('cpu'),
                             memory=request.data.get('memory'), hdd=request.data.get('hdd'))
        return Response(status=status.HTTP_201_CREATED)


    def put(self, request, *args, **kwargs):
        service = CalipsoAvailableImagesServices()
        public_name = self.kwargs.get('public_name')
        service.modify_image(public_name=public_name, image=request.data.get('image'),
                             port_hook=request.data.get('port_hook'), logs_er=request.data.get('logs_er'),
                             protocol=request.data.get('protocol'), cpu=request.data.get('cpu'),
                             memory=request.data.get('memory'), hdd=request.data.get('hdd'))
        return Response(status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        service = CalipsoAvailableImagesServices()
        service.delete_image(self.kwargs.get('public_name'))
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetAllImages(APIView):
    """
       get:
       Return all images
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        service = CalipsoAvailableImagesServices()
        images = service.get_all_images()
        serializer_class = CalipsoImageSerializer(images, many=True)
        return Response(serializer_class.data)
