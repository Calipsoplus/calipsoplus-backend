from calipsoplus.settings import *

DEBUG = False
CORS_ORIGIN_ALLOW_ALL = False

ALLOWED_HOSTS = ['calipsotest.cells.es']

CORS_ORIGIN_WHITELIST = ['calipsotest.cells.es', ]

DJANGO_ENV = 'DEMO'

# docker location
DOCKER_URL_DAEMON = "tcp://calipsotest.cells.es:2375"
REMOTE_MACHINE_IP = "calipsotest.cells.es"

# logs
LOGGING['loggers']['django']['handlers'] = ['file']
LOGGING['loggers']['django_cron']['handlers'] = ['file']
LOGGING['loggers']['apprest']['handlers'] = ['file']

# backend
BACKEND_CALIPSO = "https://calipsotest.cells.es"

# frontend
FRONTEND_CALIPSO = "https://calipsotest.cells.es"

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
