import logging

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

logger = logging.getLogger(__name__)


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
    logger.debug("get, get_umbrella_frontend, redirect to: %s", settings.FRONTEND_CALIPSO + '/autologin')
    return redirect(settings.FRONTEND_CALIPSO + '/autologin')


@api_view(["GET", ])
def get_umbrella_login(request):
    logger.debug("get, get_umbrella_login, redirect to: %s", settings.UMBRELLA_LOGIN)
    return redirect(settings.UMBRELLA_LOGIN)


@api_view(['POST'])
def login_umbrella_by_hash(request):
    logger.debug("post, login_umbrella_by_hash")
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
        logout(request)
        login(request, user, backend='apprest.views.auth_umbrella.ExternalUmbrellaServiceAuthenticationBackend')
        return JSONResponse('Login OK', status=status.HTTP_200_OK)


@api_view(["GET", ])
def get_umbrella_logout_local(request):
    logout(request)
    return JSONResponse("ok logout", status=status.HTTP_200_OK)


@api_view(['POST'])
def find_umbrella_hash_in_user_office_fake(request):
    logger.debug("post, find_umbrella_hash_in_user_office_fake, redirect")
    try:
        hash = request.data['EAAHash']

        # if hash exists, ok
        return JSONResponse('Login OK', status=status.HTTP_200_OK)
        #return JSONResponse('Not Found', status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JSONResponse("error:%s" % e, status=400)