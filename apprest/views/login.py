from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view

from apprest.services.experiment import CalipsoExperimentsServices
from apprest.utils.request import JSONResponse
from calipsoplus.settings_calipso import ALLOW_LOCAL_AUTHENTICATION


@api_view(['POST'])
def login_user(request):
    logout(request)
    try:
        username = request.data['username']
        password = request.data['password']

    except Exception as e:
        return JSONResponse(
            "Expected 'username' and 'password'",
            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user, backend='apprest.views.auth.ExternalServiceAuthenticationBackend')

        return JSONResponse('Login OK', status=status.HTTP_200_OK)
    else:
        return JSONResponse('Unable to authenticate', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def logout_user(request):
    logout(request)
    return JSONResponse('Logout OK', status=status.HTTP_200_OK)


@api_view(['GET'])
def get_calipso_settings(request):
    json_settings_data = {'local_auth': (ALLOW_LOCAL_AUTHENTICATION == 1)}
    return JsonResponse(json_settings_data)


@api_view(['GET'])
def get_login_type(request):

    calipso_experiment_services = CalipsoExperimentsServices()
    json_settings_data = calipso_experiment_services.get_external_is_staff(request.user.username)
    return JsonResponse(json_settings_data)

