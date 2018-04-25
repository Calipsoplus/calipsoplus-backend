import logging

from rest_framework import status

from apprest.models.experiment import CalipsoExperiment
from apprest.models.user import CalipsoUser
from apprest.serializers.experiment import CalipsoExperimentSerializer
from apprest.services.experiment import CalipsoExperimentsServices
from apprest.utils.request import JSONResponse, ErrorFormatting

service = CalipsoExperimentsServices()
logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


def get_experiments_from_user_id(request, user_id):
    if request.method == 'GET':
        try:
            logger.debug('get_experiments_from_user_id (user_id=%s)' % user_id)
            experiments = service.get_user_experiments(user_id=user_id)
            serializer = CalipsoExperimentSerializer(experiments, many=True)
            return JSONResponse(serializer.data)
        except CalipsoUser.DoesNotExist as dne:
            logger.error(errorFormatting.format(dne))
            return JSONResponse({'error': errorFormatting.format(dne)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
