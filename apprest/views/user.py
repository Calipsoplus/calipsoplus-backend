import logging

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from apprest.models.user import CalipsoUser
from apprest.serializers.experiment import CalipsoExperimentSerializer
from apprest.serializers.user import CalipsoUserSerializer
from apprest.services.user import CalipsoUserServices

from apprest.utils.request import JSONResponse, ErrorFormatting

service = CalipsoUserServices()
logger = logging.getLogger(__name__)
errorFormatting = ErrorFormatting()


@login_required
def get_all_users(request):
    if request.method == 'GET':
        try:
            users = service.get_all_users()
            serializer = CalipsoUserSerializer(users, many=True)
            return JSONResponse(serializer.data)
        except CalipsoUser.DoesNotExist as dne:
            logger.error(errorFormatting.format(dne))
            return JSONResponse({'error': errorFormatting.format(dne)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required
def get_user(request, user_id):

    if request.method == 'GET':
        try:
            logger.debug('get_user (user_id=%s)' % user_id)

            user = service.get_user(user_id=user_id)
            serializer = CalipsoUserSerializer(user)
            return JSONResponse(serializer.data)
        except CalipsoUser.DoesNotExist as dne:
            logger.error(errorFormatting.format(dne))
            return JSONResponse({'error': errorFormatting.format(dne)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(errorFormatting.format(e))
            return JSONResponse({'error': errorFormatting.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required
def get_user_experiments(request, user_id):
    if request.method == 'GET':
        try:
            logger.debug('get_user_experiments (user_id=%s)' % user_id)
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
