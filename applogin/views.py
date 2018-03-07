"""
from django.contrib.auth import authenticate,logout, login
from django.http import HttpResponseRedirect

from rest_framework import status

from apprest.serializers.user import CalipsoUserSerializer
from apprest.utils.request import JSONResponse


def login_user(request):

    if request.method == 'POST':
        logout(request)

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                serializer = CalipsoUserSerializer(user)
                return JSONResponse(serializer.data)
        return JSONResponse({'error': 'HTTP_401_UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)

    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
"""
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render


def index(request):
    form = AuthenticationForm(data=request.POST)
    return render(request, 'index.html',{'form': form})
