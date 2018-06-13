from django.conf.urls import url, include
from django.urls import path

from apprest.views.experiment import GetExperimentsByUserName
from apprest.views.facility import GetAllFacilities
from apprest.views.login import login_user, logout_user

urlpatterns = [
    url(r'^container/', include('apprest.urls.container')),
    path('experiments/<username>/', GetExperimentsByUserName.as_view()),
    path('facility/', GetAllFacilities.as_view()),
    path('login/', login_user),
    path('logout/', logout_user),
]
