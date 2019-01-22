import logging

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apprest.serializers.container import CalipsoContainerSerializer
from apprest.services.container import CalipsoContainersServices
from apprest.services.guacamole import CalipsoGuacamoleServices
from apprest.services.image import CalipsoAvailableImagesServices
from apprest.services.session import CalipsoSessionsServices

from apprest.utils.request import JSONResponse, ErrorFormatting

from django.conf import settings

container_service = CalipsoContainersServices()
guacamole_service = CalipsoGuacamoleServices()
session_service = CalipsoSessionsServices()
image_service = CalipsoAvailableImagesServices()

logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication,))
def rm_container(request, username, container_name):
    if username != request.user.username:
        return JSONResponse("username mismatch", status=status.HTTP_403_FORBIDDEN)
    try:
        container_data = container_service.rm_container(container_name)
        try:
            serializer = CalipsoContainerSerializer(container_data)
            return JSONResponse(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.debug(errorFormatting.format(e))
            return JSONResponse([], status=status.HTTP_200_OK)

    except Exception as e:
        logger.debug(errorFormatting.format(e))
        return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication,))
def stop_container(request, username, container_name):
    if username != request.user.username:
        return JSONResponse("username mismatch", status=status.HTTP_403_FORBIDDEN)
    try:
        container_data = container_service.stop_container(container_name)
        try:
            serializer = CalipsoContainerSerializer(container_data)
            return JSONResponse(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.debug(errorFormatting.format(e))
            return JSONResponse([], status=status.HTTP_200_OK)

    except Exception as e:
        logger.debug(errorFormatting.format(e))
        return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def run_container(request, username, experiment, public_name):
    experiment_session = experiment.split("~")

    if len(experiment_session) == 2:
        experiment_serial_number = experiment_session[0]
        session_number = experiment_session[1]
    else:
        experiment_serial_number = experiment
        session_number = experiment

    logger.debug("Running session:%s from experiment:%s" % (experiment_serial_number, session_number))

    if username != request.user.username:
        return JSONResponse("username mismatch", status=status.HTTP_403_FORBIDDEN)

    try:
        container = container_service.run_container(username, session_number, public_name)
    except Exception as e:
        logger.debug("Error after run_container : %s " % e)
        return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_204_NO_CONTENT)

    image_selected = image_service.get_available_image(public_name=public_name)[0]

    logger.debug("Searching... port")

    try:
        port = int(container.container_info['NetworkSettings']['Ports'][image_selected.port_hook][0]['HostPort'])
    except Exception as e:
        port = 0

    container.container_info = experiment_serial_number
    container.save()

    serializer = CalipsoContainerSerializer(container)

    logger.debug("Selected port: %d" % port)

    try:

        params = {'guacamole_username': container.guacamole_username,
                  'guacamole_password': container.guacamole_password,
                  'guacamole_connection_name': container.container_name,
                  'guacamole_protocol': image_selected.protocol,
                  'vnc_password': container.vnc_password,
                  'container_ip': settings.REMOTE_MACHINE_IP,
                  'container_port': port}

        guacamole_service.create_connection(params)

    except Exception as e:
        logger.debug(errorFormatting.format(e))
        return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)


class GetContainersByUserName(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoContainerSerializer
    pagination_class = None

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username == self.request.user.username:
            return container_service.list_container(self.request.user.username)
        else:
            raise PermissionDenied

    def dispatch(self, *args, **kwargs):
        return super(GetContainersByUserName, self).dispatch(*args, **kwargs)
