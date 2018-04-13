from django.conf.urls import url

from apprest.views import experiment, container

urlpatterns = [
    url(r'^(?P<user_id>\d+)/experiments/$', experiment.get_experiments_from_user_id),
    url(r'^(?P<user_id>\d+)/experiments/(?P<experiment_id>\d+)/add/$', container.create),
]
