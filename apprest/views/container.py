import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from apprest.serializers.container import CalipsoContainerSerializer
from apprest.services.container import CalipsoContainersServices
from apprest.services.guacamole import CalipsoGuacamoleServices

from apprest.utils.request import JSONResponse, ErrorFormatting

GUACAMOLE_USERNAME = "alexcamps"

GUACAMOLE_USER_PASSORD = "password"

PROTOCOL = "vnc"

VNCPASSWORD = "vncpassword"

HOST_DOCKER_IP = "192.168.33.13"

container_service = CalipsoContainersServices()
guacamole_service = CalipsoGuacamoleServices()

logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


def index(request):
    return HttpResponse("Hello, world. You're at the docker index.")


def rm_container(request, container_id):
    container_data = container_service.rm_container(container_id)
    return HttpResponse(container_data)


def stop_container(request, container_id):
    container_data = container_service.stop_container(container_id)
    return HttpResponse(container_data)


@csrf_exempt
def run_container(request):
    if request.method == 'POST':
        try:
            container = container_service.run_container(GUACAMOLE_USERNAME, GUACAMOLE_USER_PASSORD, VNCPASSWORD)
            serializer = CalipsoContainerSerializer(container)
            try:
                port = int(container.container_info['NetworkSettings']['Ports']['5901/tcp'][0]['HostPort'])

                guacamole_service.create_connection(GUACAMOLE_USERNAME, GUACAMOLE_USER_PASSORD,
                                                    container.container_name,
                                                    PROTOCOL, VNCPASSWORD, HOST_DOCKER_IP, port)

            except Exception as e:
                logger.error(errorFormatting.format(e))
                return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)

            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)