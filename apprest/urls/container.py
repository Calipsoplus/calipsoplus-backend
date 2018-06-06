from django.urls import path

from apprest.views import container
from apprest.views.container import GetContainersByUserName

urlpatterns = [
    path('run/<username>/<experiment>/', container.run_container, name='run_container'),
    path('rm/<username>/<container_name>/', container.rm_container, name='rm_container'),
    path('stop/<username>/<container_name>/', container.stop_container, name='stop_container'),
    path('list/<username>/', GetContainersByUserName.as_view()),
]
