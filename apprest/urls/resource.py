from django.urls import path

from apprest.views.resource import GetResourcesByUserName, run_resource, rm_resource, stop_resource

urlpatterns = [
    path('list/<username>/', GetResourcesByUserName.as_view(), name='list_resource'),
    path('run/<username>/<experiment>/<public_name>/', run_resource, name='run_resource'),
    path('rm/<username>/<resource_name>/<public_name>/', rm_resource, name='rm_resource'),
    path('stop/<username>/<resource_name>/<public_name>/', stop_resource, name='stop_resource'),

]
