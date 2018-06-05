from django.conf.urls import url

from apprest.views.experiment import GetExperimentsByUserName

urlpatterns = [
  #  url(r'^(?P<username>\w{1,50})/experiment/$', GetExperimentsByUserName.as_view()),
]
