from django.conf.urls import url

from apprest.views.container import create, delete

urlpatterns = [
    url(r'^add/$', create),
    url(r'^(?P<container_uid>\d+)/remove/$', delete),
]
