from calipsoplus.settings import *

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = False

ALLOWED_HOSTS = ['.cells.es']

CORS_ORIGIN_WHITELIST = ['misapptest.cells.es', ]

DJANGO_ENV = 'TEST'

# docker location
DOCKER_URL_DAEMON = "tcp://calipsotest.cells.es:2375"
REMOTE_MACHINE_IP = "calipsotest.cells.es"

# logs
LOGGING['loggers']['django']['handlers'] = ['file']
LOGGING['loggers']['django_cron']['handlers'] = ['file']
LOGGING['loggers']['apprest']['handlers'] = ['file']

# backend
BACKEND_CALIPSO = "https://misapptest.cells.es/calipsoplus-services"

# frontend
FRONTEND_CALIPSO = "https://misapptest.cells.es/calipsoplus"

# umbrella_logout
UMBRELLA_LOGOUT = BACKEND_CALIPSO + "/Shibboleth.sso/Logout?return=" + FRONTEND_CALIPSO

# umbrella_login
UMBRELLA_LOGIN = BACKEND_CALIPSO + "/Shibboleth.sso/Login?target=" + BACKEND_CALIPSO + "/calipsoplus-services/umbrella/frontend/"

# User Office backend API login
BACKEND_UO_LOGIN = "https://misapptest.cells.es/duo-services/login/"
BACKEND_UO_HASH = "https://misapptest.cells.es/duo-services/login/umbrella/"
