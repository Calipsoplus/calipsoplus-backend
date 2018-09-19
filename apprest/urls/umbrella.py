from django.urls import path

from apprest.views.umbrella import get_umbrella_session_hash, login_umbrella_by_hash, get_umbrella_login, \
    get_umbrella_frontend, get_umbrella_logout_local

urlpatterns = [
    path('session/', get_umbrella_session_hash),
    path('login/', get_umbrella_login),
    path('logout/', get_umbrella_logout_local),
    path('frontend/', get_umbrella_frontend),
    path('wuo/', login_umbrella_by_hash),
]