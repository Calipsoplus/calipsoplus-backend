from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from rest_framework import status

from apprest.models.user import CalipsoUser
from apprest.serializers.user import CalipsoUserSerializer
from apprest.utils.request import JSONResponse


@csrf_exempt
def login_calipso_user(request):
    if request.method == 'POST':
        logout(request)

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                calipso_user = CalipsoUser.objects.get(user=user)
                serializer = CalipsoUserSerializer(calipso_user)
                return JSONResponse(serializer.data)
        return JSONResponse({'error': 'HTTP_401_UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)

    return JSONResponse({'error': 'METHOD NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def logout_calipso_user(request):
    logout(request)
    return JSONResponse({'message': 'logout done'}, status=status.HTTP_200_OK)