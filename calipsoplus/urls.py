from django.conf.urls import url, include
from django.urls import path

from apprest.views.experiment import GetExperimentsByUserName
from apprest.views.facility import GetAllFacilities
from apprest.views.favorite import CalipsoExperimentFavorite
from apprest.views.image import GetUsedQuotaFromUser, GetInfoImage, GetAllImages
from apprest.views.login import login_user, logout_user, get_calipso_settings, get_login_authorization
from apprest.views.quota import QuotaView

urlpatterns = [
    url(r'^resource/', include('apprest.urls.resource')),
    url(r'^umbrella/', include('apprest.urls.umbrella')),
    path('experiments/<username>/', GetExperimentsByUserName.as_view()),
    url(r'^favorite/(?P<pk>[0-9]+)/$', CalipsoExperimentFavorite.as_view()),
    path('quota/<username>/', QuotaView.as_view()),
    path('used_quota/<username>/', GetUsedQuotaFromUser.as_view()),
    path('images/', GetAllImages.as_view()),
    path('image/<public_name>/', GetInfoImage.as_view()),
    path('images/', GetAllImages.as_view()),
    path('facility/', GetAllFacilities.as_view()),
    path('login/', login_user),
    path('logout/', logout_user),
    path('settings/', get_calipso_settings),
    path('login/type/', get_login_authorization)
]
