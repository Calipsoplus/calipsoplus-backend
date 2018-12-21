# define generic quota per user
MAX_CONTAINER_PER_USER = 5
MAX_RAM_PER_USER = "30G"
MAX_CPU_PER_USER = 10
MAX_STORAGE_PER_USER = "80G"

# define limit max experiments per page
PAGE_SIZE_EXPERIMENTS = 7

# 0: This would only allow Umbrella authentication. By default, the system does only allow Umbrella authentication.
# 1: This would allow the user to show the form in order to authenticate locally
ALLOW_LOCAL_AUTHENTICATION = 1

# Both volumes should be built dynamically, but root of both of them must be declared as settings variables
# (e.g EXPERIMENTS_DATASETS_ROOT - for the read-only - and EXPERIMENTS_OUTPUT - for the results)--
EXPERIMENTS_DATASETS_ROOT = "/tmp/data"
EXPERIMENTS_OUTPUT = "/tmp/results"

# which indicates whether getting the information from a REST endpoint (1) or the DB (0)
DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL = 0
