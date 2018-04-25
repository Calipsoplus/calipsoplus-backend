"""calipsoplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from apprest.views import login

urlpatterns = [
    url(r'^users/', include('apprest.urls.user')),
    url(r'^facilities/', include('apprest.urls.facility')),
    url(r'^containers/', include('apprest.urls.container')),
    url(r'^login/$', login.login_calipso_user, name='login'),
    url(r'^logout/$', login.logout_calipso_user),
]
