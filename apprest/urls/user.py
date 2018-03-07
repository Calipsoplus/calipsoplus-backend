from django.conf.urls import url

from apprest.views import user

urlpatterns = [
    url(r'^all/$', user.get_all_users),
    url(r'^(?P<user_id>\d+)/$', user.get_user),
    url(r'^(?P<user_id>\d+)/experiments/$', user.get_user_experiments),
]
