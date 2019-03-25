from django.shortcuts import render


def index(request):
    return render(request, 'apprest/oidc_authentication_init.html')
