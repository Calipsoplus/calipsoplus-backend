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

TESTING_MODE = True
