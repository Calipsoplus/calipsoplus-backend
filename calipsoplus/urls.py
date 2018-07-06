from django.conf.urls import url, include
from django.urls import path

from apprest.views.experiment import GetExperimentsByUserName
from apprest.views.facility import GetAllFacilities
from apprest.views.image import GetUsedQuotaFromUser, GetInfoImage
from apprest.views.login import login_user, logout_user
from apprest.views.quota import GetDefaultUserQuotasFromUser

urlpatterns = [
    url(r'^container/', include('apprest.urls.container')),
    path('experiments/<username>/', GetExperimentsByUserName.as_view()),
    path('quota/<username>/', GetDefaultUserQuotasFromUser.as_view()),
    path('used_quota/<username>/', GetUsedQuotaFromUser.as_view()),
    path('image/<public_name>/', GetInfoImage.as_view()),
    path('facility/', GetAllFacilities.as_view()),
    path('login/', login_user),
    path('logout/', logout_user),
]