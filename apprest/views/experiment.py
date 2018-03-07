import logging

from rest_framework import status

from apprest.models.experiments import CalipsoExperiment
from apprest.serializers.experiment import CalipsoExperimentSerializer
from apprest.services.experiment import CalipsoExperimentsServices
from apprest.utils.request import JSONResponse, ErrorFormatting

service = CalipsoExperimentsServices()
logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


def get_all_experiments(request):
    if request.method == 'GET':
        try:
            experiments = service.get_all_experiments()
            serializer = CalipsoExperimentSerializer(experiments, many=True)
            return JSONResponse(serializer.data)
        except CalipsoExperiment.DoesNotExist as dne:
            logger.error(errorFormatting.format(dne))
            return JSONResponse({'error': errorFormatting.format(dne)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
"""
def get_experiments_from_id_user(request, user_id):
    if request.method == 'GET':
        try:
            logger.debug('get_experiments_from_id_user (USER_ID=%s)' % user_id)
            experiments = service.get_experiments_from_user(user_id=user_id)
            serializer = CalipsoExperimentSerializer(experiments, many=True)
            return JSONResponse(serializer.data)
        except CalipsoExperiment.DoesNotExist as dne:
            logger.error(errorFormatting.format(dne))
            return JSONResponse({'error': errorFormatting.format(dne)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
"""
def get_experiment(request, experiment_id):
    if request.method == 'GET':
        try:
            logger.debug('get_experiment (experiment_id=%s)' % experiment_id)
            experiment = service.get_experiment(experiment_id=experiment_id)
            serializer = CalipsoExperimentSerializer(experiment)
            return JSONResponse(serializer.data)
        except CalipsoExperiment.DoesNotExist as dne:
            logger.error(errorFormatting.format(dne))
            return JSONResponse({'error': errorFormatting.format(dne)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)