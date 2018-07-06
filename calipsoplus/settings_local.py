from calipsoplus.settings import *

DEBUG = True

ALLOWED_HOSTS = ['192.168.33.11']

DJANGO_ENV = 'LOCAL'

# docker location
DOCKER_URL_DAEMON = "tcp://192.168.33.13:2375"
REMOTE_MACHINE_IP = "192.168.33.13"

# User Office backend API login
BACKEND_UO = "https://misapptest.cells.es/duo-services/login/"

# logs
LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['django_cron']['handlers'] = ['console']
LOGGING['loggers']['apprest']['handlers'] = ['console']