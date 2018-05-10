import logging
import pdb

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from apprest.serializers.container import CalipsoContainerSerializer
from apprest.services.container import CalipsoContainersServices
from apprest.services.guacamole import CalipsoGuacamoleServices

from apprest.utils.request import JSONResponse, ErrorFormatting
from calipsoplus.settings import HOST_DOCKER_IP

PROTOCOL = "vnc"


container_service = CalipsoContainersServices()
guacamole_service = CalipsoGuacamoleServices()

logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


def index(request):
    return HttpResponse("Hello, world. You're at the docker index.")


def rm_container(request, container_name):
    if request.method == 'GET':
        try:
            container_data = container_service.rm_container(container_name)
            try:
                serializer = CalipsoContainerSerializer(container_data)
                return JSONResponse(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(errorFormatting.format(e))
                return JSONResponse([], status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def stop_container(request, container_name):
    if request.method == 'GET':
        try:
            container_data = container_service.stop_container(container_name)
            serializer = CalipsoContainerSerializer(container_data)
            return JSONResponse(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
def run_container(request, username, experiment):
    if request.method == 'POST':
        try:
            container = container_service.run_container(username, experiment)
            serializer = CalipsoContainerSerializer(container)
            try:
                port = int(container.container_info['NetworkSettings']['Ports']['5901/tcp'][0]['HostPort'])

                guacamole_service.create_connection(guacamole_username=container.guacamole_username,
                                                    guacamole_password=container.guacamole_password,
                                                    guacamole_connection_name=container.container_name,
                                                    guacamole_protocol=PROTOCOL,
                                                    vnc_password=container.vnc_password,
                                                    container_ip=HOST_DOCKER_IP,
                                                    container_port=port)

            except Exception as e:
                logger.error(errorFormatting.format(e))
                return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)

            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def list_container(request, username):
    if request.method == 'GET':
        try:
            container_data = container_service.list_container(username=username)

            try:
                serializer = CalipsoContainerSerializer(container_data, many=True)
                return JSONResponse(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)