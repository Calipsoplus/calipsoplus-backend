from django.conf.urls import url, include
from django.urls import path

from apprest.views.auth import is_user_authenticated
from apprest.views.experiment import GetExperimentsByUserName
from apprest.views.favorite import CalipsoExperimentFavorite
from apprest.views.image import GetInfoImage, GetAllImages
from apprest.views.login import login_user, logout_user, get_calipso_settings, get_login_authorization
from apprest.views.quota import QuotaView, GetUsedQuotaFromUser
from apprest.views.user import GetUser, GetAllUsers, UserAdmin
from apprest.views.container import ContainerInfo, ActiveContainers, UserContainers, AllContainersInfo
from apprest.views.openidtest import index
from apprest.plugins.icat.views.ICAT import GetInvestigationUsers

urlpatterns = [
    url(r'^resource/', include('apprest.urls.resource')),
    url(r'^umbrella/', include('apprest.urls.umbrella')),
    url(r'^favorite/(?P<pk>[0-9]+)/$', CalipsoExperimentFavorite.as_view()),
    url(r'^oidc/', include('mozilla_django_oidc.urls')),
    path('authenticated/', is_user_authenticated, name='is_auth'),
    path('activecontainers/', ActiveContainers.as_view()),
    path('containers/', AllContainersInfo.as_view()),
    path('containers/<id>', ContainerInfo.as_view()),
    path('experiments/<investigation_id>/users', GetInvestigationUsers.as_view()),
    path('images/', GetAllImages.as_view()),
    path('images/<public_name>/', GetInfoImage.as_view()),
    path('login/', login_user),
    path('login/type/', get_login_authorization),
    path('logout/', logout_user),
    path('openidtest/', index, name='index'),
    path('quota/<username>/', QuotaView.as_view()),
    path('settings/', get_calipso_settings),
    path('used_quota/<username>/', GetUsedQuotaFromUser.as_view()),
    path('users/', GetAllUsers.as_view()),
    path('users/<username>/', GetUser.as_view()),
    path('users/<username>/admin', UserAdmin.as_view()),
    path('users/<username>/containers/', UserContainers.as_view()),
    path('users/<username>/experiments/', GetExperimentsByUserName.as_view()),
]
