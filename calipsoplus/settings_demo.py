from calipsoplus.settings import *

DEBUG = False

ALLOWED_HOSTS = ['.cells.es']

DJANGO_ENV = 'DEMO'

# docker location
DOCKER_URL_DAEMON = "tcp://calipsotest.cells.es:2375"
REMOTE_MACHINE_IP = "calipsotest.cells.es"

# User Office backend API login
BACKEND_UO = "https://misapptest.cells.es/duo-services/login/"

# logs
LOGGING['loggers']['django']['handlers'] = ['file']
LOGGING['loggers']['django_cron']['handlers'] = ['file']
LOGGING['loggers']['apprest']['handlers'] = ['file']
