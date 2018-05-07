from django.conf.urls import url

from apprest.views import experiment

urlpatterns = [
    url(r'^(?P<user_id>\d+)/experiment/$', experiment.get_experiments_from_username),
]
