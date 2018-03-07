import logging

from rest_framework import status

from apprest.models.facilities import CalipsoFacility
from apprest.serializers.facility import CalipsoFacilitySerializer
from apprest.services.facility import CalipsoFacilityServices

from apprest.utils.request import JSONResponse, ErrorFormatting

service = CalipsoFacilityServices()
logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


def get_all_facilities(request):

    if request.method == 'GET':
        try:
            facilities = service.get_all_facilities()
            serializer = CalipsoFacilitySerializer(facilities, many=True)
            return JSONResponse(serializer.data)
        except CalipsoFacility.DoesNotExist as dne:
            logger.error(errorFormatting.format(dne))
            return JSONResponse({'error': errorFormatting.format(dne)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
