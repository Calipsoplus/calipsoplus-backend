from calipsoplus.settings import *


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
LOGGING['loggers']['apprest']['handlers'] = ['file']

TESTING_MODE = True

# docker location
DOCKER_URL_DAEMON = "tcp://192.168.33.13:2375"
REMOTE_MACHINE_IP = "192.168.33.13"