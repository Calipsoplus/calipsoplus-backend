from django.conf.urls import url

from apprest.views import experiment

urlpatterns = [
    url(r'^(?P<username>\w{1,50})/experiment/$', experiment.get_experiments_from_username),
]
