import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apprest.models import CalipsoResourcesType, CalipsoAvailableImages
from apprest.serializers.container import CalipsoContainerSerializer
from apprest.services.container import CalipsoContainersServices
from apprest.services.guacamole import CalipsoGuacamoleServices

from apprest.services.resources import GenericCalipsoResourceService
from apprest.services.session import CalipsoSessionsServices

from apprest.utils.request import ErrorFormatting, JSONResponse

from apprest.utils.resources import ResourceType

from calipsoplus.settings_calipso import REMOTE_PODS_MACHINE_IP

container_service = CalipsoContainersServices()
guacamole_service = CalipsoGuacamoleServices()
session_service = CalipsoSessionsServices()

logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication,))
def rm_resource(request, username, resource_name, public_name):
    image_selected = CalipsoAvailableImages.objects.get(public_name=public_name)
    try:
        resource_type = CalipsoResourcesType.objects.get(pk=image_selected.resource_type.id)
    except Exception as e:
        logger.debug("CalipsoResourcesType.objects.get e:%s" % e)
        raise NotFound

    resource_service = GenericCalipsoResourceService(resource_type.resource_type)

    if username != request.user.username:
        return JSONResponse("username mismatch", status=status.HTTP_403_FORBIDDEN)
    try:
        resource_data = resource_service.rm_resource(resource_name)
        try:
            serializer = CalipsoContainerSerializer(resource_data)
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
def stop_resource(request, username, resource_name, public_name):
    image_selected = CalipsoAvailableImages.objects.get(public_name=public_name)
    try:
        resource_type = CalipsoResourcesType.objects.get(pk=image_selected.resource_type.id)
    except Exception as e:
        logger.debug("CalipsoResourcesType.objects.get e:%s" % e)
        raise NotFound

    resource_service = GenericCalipsoResourceService(resource_type.resource_type)

    if username != request.user.username:
        return JSONResponse("username mismatch", status=status.HTTP_403_FORBIDDEN)
    try:
        resource_data = resource_service.stop_resource(resource_name)
        try:
            serializer = CalipsoContainerSerializer(resource_data)
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
def run_resource(request, username, experiment, public_name):
    image_selected = CalipsoAvailableImages.objects.get(public_name=public_name)
    try:
        resource_type = CalipsoResourcesType.objects.get(pk=image_selected.resource_type.id)
    except Exception as e:
        logger.debug("CalipsoResourcesType.objects.get e:%s" % e)
        raise NotFound

    resource_service = GenericCalipsoResourceService(resource_type.resource_type)

    experiment_session = experiment.split("~")

    if len(experiment_session) == 2:
        experiment_proposal_id = experiment_session[0]
        session_number = experiment_session[1]
    else:
        experiment_proposal_id = experiment
        session_number = experiment

    logger.debug("Running session:%s from experiment:%s" % (experiment_proposal_id, session_number))

    if username != request.user.username:
        return JSONResponse("username mismatch", status=status.HTTP_403_FORBIDDEN)
    try:
        resource = resource_service.run_resource(username=username, experiment=session_number,
                                                 public_name=public_name)

    except Exception as e:
        logger.debug("Error after run_container : %s " % e)
        return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_204_NO_CONTENT)

    logger.debug("Searching... port")

    container_ip = settings.REMOTE_MACHINE_IP
    port = resource.host_port

    if resource_type.resource_type == ResourceType.kubernetes:
        container_ip = REMOTE_PODS_MACHINE_IP
        port = int(resource.host_port)

    if port == 0:
        try:
            port = int(resource.container_info['NetworkSettings']['Ports'][image_selected.port_hook][0]['HostPort'])
        except Exception as e:
            port = 0

    resource.container_info = experiment_proposal_id
    resource.save()

    serializer = CalipsoContainerSerializer(resource)

    logger.debug("Selected port: %s" % str(port))

    try:

        params = {'guacamole_username': resource.guacamole_username,
                  'guacamole_password': resource.guacamole_password,
                  'guacamole_connection_name': resource.container_name,
                  'guacamole_protocol': image_selected.protocol,
                  'vnc_password': resource.vnc_password,
                  'container_ip': container_ip,
                  'container_port': port}

        guacamole_service.create_connection(params)

    except Exception as e:
        logger.debug(errorFormatting.format(e))
        return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)


class GetResourcesByUserName(ListAPIView):
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
        return super(GetResourcesByUserName, self).dispatch(*args, **kwargs)
