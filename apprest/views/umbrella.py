import requests
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.decorators import api_view

from apprest.services.user import CalipsoUserServices
from apprest.utils.request import JSONResponse

from django.conf import settings

user_service = CalipsoUserServices()


@api_view(["GET", ])
def get_umbrella_session_hash(request):
    json_umbrella_session = user_service.get_umbrella_session_hash(request)

    if json_umbrella_session is None:
        return JsonResponse({'msg': 'session not found'}, status=404)
    else:
        resp = JsonResponse(json_umbrella_session)
        return resp


@api_view(["GET", ])
def get_umbrella_frontend(request):
    return redirect(settings.FRONTEND_CALIPSO + '/autologin/')


@api_view(["GET", ])
def get_umbrella_login(request):
    return redirect(settings.UMBRELLA_LOGIN)


@api_view(['POST'])
def login_umbrella_by_hash(request):
    logout(request)
    try:
        eaa_hash = request.data['EAAHash']
        uid = request.data['uid']
    except Exception as e:
        return JSONResponse(
            "Expected 'EAAHash' error:%s" % e,
            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, uid=uid, eaa_hash=eaa_hash)

    if user is None:
        return JsonResponse({'msg': 'user not found'}, status=404)
    else:
        login(request, user, backend='apprest.views.auth_umbrella.ExternalUmbrellaServiceAuthenticationBackend')
        return JSONResponse('Login OK', status=status.HTTP_200_OK)


@api_view(["GET", ])
def get_umbrella_logout_local(request):
    logout(request)
    return redirect(settings.UMBRELLA_LOGOUT)


@api_view(['POST'])
def find_umbrella_hash_in_user_office_fake(request):
    try:
        hash = request.data['EAAHash']
        uid = request.data['uid']

        # if hash exists, ok
        return JSONResponse('Login OK', status=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse("error:%s" % e, status=400)