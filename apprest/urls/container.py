from django.urls import path

from apprest.views import container

urlpatterns = [
    path('', container.index, name='index'),
    path('run', container.run_container, name='run_container'),
    path('rm/<container_id>/', container.rm_container, name='rm_container'),
    path('stop/<container_id>/', container.stop_container, name='stop_container'),
]
