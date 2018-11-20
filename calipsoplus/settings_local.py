from calipsoplus.settings import *

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = False

ALLOWED_HOSTS = ['192.168.33.11', 'vagrant-ubuntu-trusty-64']

CORS_ORIGIN_WHITELIST = ['192.168.33.10:8001', '192.168.33.11:443', '192.168.33.11:8000', '192.168.33.11',
                         'vagrant-ubuntu-trusty-64']

DJANGO_ENV = 'LOCAL'

# docker location
DOCKER_URL_DAEMON = "tcp://192.168.33.13:2375"
REMOTE_MACHINE_IP = "192.168.33.13"

# logs
LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['django_cron']['handlers'] = ['console']
LOGGING['loggers']['apprest']['handlers'] = ['console']

# backend
BACKEND_CALIPSO = "https://vagrant-ubuntu-trusty-64"

# frontend
FRONTEND_CALIPSO = "http://192.168.33.10:8001"

# umbrella_logout
UMBRELLA_LOGOUT = BACKEND_CALIPSO + "/Shibboleth.sso/Logout"

# umbrella_login
UMBRELLA_LOGIN = BACKEND_CALIPSO + "/Shibboleth.sso/Login?target=" + BACKEND_CALIPSO + "/calipso/umbrella/frontend/"

# User Office backend API login
BACKEND_UO_LOGIN = "https://misapptest.cells.es/duo-services/login/"

