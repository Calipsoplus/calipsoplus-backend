from calipsoplus.settings import *

ALLOWED_HOSTS = ['192.168.33.11']

DJANGO_ENV = 'LOCAL'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    },
    'guacamole': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'guacamole'
    }
}

# logs
LOGGING['loggers']['apprest']['handlers'] = ['console']

TESTING_MODE = True

# docker location
DOCKER_URL_DAEMON = "tcp://192.168.33.13:2375"
REMOTE_MACHINE_IP = "192.168.33.13"

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

# which indicates the REST endpoint to be connected against, if the DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL flag is set to 1.
# Note: endpoint should contain: login, number of items (pagination), offset (from and to), and keyword (optional)
DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL_ENDPOINT = "https://misapptest.cells.es/duo-services/experiments/$USERNAME/"
