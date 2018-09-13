from calipsoplus.settings import *

ALLOWED_HOSTS = ['192.168.33.11']

DJANGO_ENV = 'LOCAL'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    },
    'auth_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'auth_db'
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
BACKEND_UO_HASH = BACKEND_CALIPSO + "/calipso/duo-services/hash/"