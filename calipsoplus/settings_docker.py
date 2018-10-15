from calipsoplus.settings import *

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = False

ALLOWED_HOSTS = ['web-back']

CORS_ORIGIN_WHITELIST = ['web-front','web-back']

DJANGO_ENV = 'DOCKER'

# docker location
DOCKER_URL_DAEMON = "tcp://calipsotest.cells.es:2375"
REMOTE_MACHINE_IP = "calipsotest.cells.es"

# logs
LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['django_cron']['handlers'] = ['console']
LOGGING['loggers']['apprest']['handlers'] = ['console']

# backend
BACKEND_CALIPSO = "web-back"

# frontend
FRONTEND_CALIPSO = "web-front"

# umbrella_logout
UMBRELLA_LOGOUT = BACKEND_CALIPSO + "/Shibboleth.sso/Logout?return=" + FRONTEND_CALIPSO

# umbrella_login
UMBRELLA_LOGIN = BACKEND_CALIPSO + "/Shibboleth.sso/Login?target=" + BACKEND_CALIPSO + "/calipsoplus-services/umbrella/frontend/"

# User Office backend API login
BACKEND_UO_LOGIN = "https://misapptest.cells.es/duo-services/login/"
BACKEND_UO_HASH = "https://misapptest.cells.es/duo-services/login/umbrella/"

#database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'read_default_file': os.path.join('/secret', 'default.cnf'),
        }
    },
    'guacamole': {
        'ENGINE': 'django.db.backends.mysql',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'read_default_file': os.path.join('/secret', 'guacamole.cnf'),
        },
    },
}