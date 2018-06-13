from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view

from apprest.utils.request import JSONResponse


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
        login(request, user)

        return JSONResponse('Login OK', status=status.HTTP_200_OK)
    else:
        return JSONResponse('Unable to authenticate', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def logout_user(request):
    logout(request)
    return JSONResponse('Logout OK', status=status.HTTP_200_OK)
