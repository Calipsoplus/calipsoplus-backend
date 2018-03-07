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

from applogin import views
from apprest.views import login

urlpatterns = [
    url(r'^users/', include('apprest.urls.user')),
    url(r'^facilities/', include('apprest.urls.facility')),
    url(r'^experiments/', include('apprest.urls.experiment')),
    url(r'^login/$', login.login_calipso_user, name='login'),
    url(r'^logout/$', login.logout_calipso_user),

    url(r'^$', views.index,name='index'),
]

"""
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^$', login_views.index, name='index'),


    # user accounts
     path('accounts/', include('django.contrib.auth.urls')),

    #admin site
    url(r'^admin/', admin.site.urls),

    #list experiments
    url(r'^experiments/$', login_views.list_experiments, name='experiments'),

    # my login
    url(r'^login/$', login, {'template_name': 'login.html'},name='login'),
    url(r'^logout/$', login_views.logout_user, name='logout'),

    # rest_framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


urlpatterns = [
    # url(r'^', include(router.urls)),
    path('login/', login_views.login_user),

    url(r'^logout/$', auth_views.logout, name='logout'),

    path('', auth_views.login,{'template_name': 'login.html'}, name='index'),

    path('accounts/', include('django.contrib.auth.urls')),
    
]


urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^$', login_views.main, name='main'),
    path('login/', login_views.login_user),
    path('logout/', login_views.logout_user),
    # path('main/', login_views.main),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    path('accounts/', include('django.contrib.auth.urls')),

]


"""
