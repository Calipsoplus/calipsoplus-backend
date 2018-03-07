from django.conf.urls import url

from apprest.views import facility

urlpatterns = [
    url(r'^all/$', facility.get_all_facilities),
]
