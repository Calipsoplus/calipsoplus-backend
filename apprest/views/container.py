import logging

from rest_framework import status
from rest_framework.parsers import JSONParser

from apprest.models.container import CalipsoContainer
from apprest.serializers.container import CalipsoContainerSerializer
from apprest.services.container import CalipsoContainerServices

from apprest.utils.request import JSONResponse, ErrorFormatting

service = CalipsoContainerServices()
logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


def create(request, user_id, experiment_id):
    #if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            serializer = CalipsoContainerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(errorFormatting.format(serializer.errors))
                return JSONResponse({'error': errorFormatting.format(serializer.errors)},
                                    status=status.HTTP_400_BAD_REQUEST)
        except CalipsoContainer.DoesNotExist as dne:
            logger.error(errorFormatting.format(dne))
            return JSONResponse({'error': errorFormatting.format(dne)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    #return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def delete(request, container_uid):
    if request.method == 'DELETE':
        if not container_uid:
            return JSONResponse({'error': 'container id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            container = service.get_by_pk(container_uid)
            service.delete(container)
            return JSONResponse(None, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


