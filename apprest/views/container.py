from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apprest.serializers.container import CalipsoContainerSerializer
from apprest.services.container import CalipsoContainersServices


class ContainerInfo(APIView):
    """
    get:
    Return the given container
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoContainerSerializer

    pagination_class = None

    def get(self, *args, **kwargs):
        service = CalipsoContainersServices()
        container_id = self.kwargs.get('id')
        container = service.get_container_by_id(cid=container_id)
        serializer_class = CalipsoContainerSerializer(container)
        return Response(serializer_class.data)


class ActiveContainers(APIView):
    """
    get:
    Return the given container
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoContainerSerializer

    pagination_class = None

    def get(self, *args, **kwargs):
        service = CalipsoContainersServices()
        containers = service.list_all_active_containers()
        serializer_class = CalipsoContainerSerializer(containers, many=True)
        return Response(serializer_class.data)


class UserContainers(APIView):
    """
    get:
    Return the given container
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoContainerSerializer

    pagination_class = None

    def get(self, *args, **kwargs):
        service = CalipsoContainersServices()
        username = self.kwargs.get('username')
        containers = service.list_container(username)
        serializer_class = CalipsoContainerSerializer(containers, many=True)
        return Response(serializer_class.data)
