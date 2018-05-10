from django.urls import path

from apprest.views import container

urlpatterns = [
    path('', container.index, name='index'),
    path('run/<username>/<experiment>/', container.run_container, name='run_container'),
    path('rm/<container_name>/', container.rm_container, name='rm_container'),
    path('stop/<container_name>/', container.stop_container, name='stop_container'),
    path('list/<username>/', container.list_container, name='list_container'),
]
