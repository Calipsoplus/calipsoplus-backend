from django.conf.urls import url

from apprest.views import experiment

urlpatterns = [
    url(r'^all/$', experiment.get_all_experiments),
    url(r'^(?P<experiment_id>\d+)/$', experiment.get_experiment),

]
