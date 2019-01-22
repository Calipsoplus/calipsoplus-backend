# CalipsoPlus Backend

The aim of this project is to provide a backend RESTful service for the CalipsoPlus JRA2 Demonstrator application.

### Contents

*  [Architecture](#architecture)
    *  [External components](#external-components)
        *  [Guacamole](#guacamole)
        *  [Local authentication provider](#local-authentication-provider)
        *  [Umbrella](#umbrella)
*  [Requirements](#requirements)
*  [Build & Development](#build-development)
    *  [Database configuration](#database-configuration)
    *  [Environment configuration files](#environment-configuration-files)
    *  [Secret key](#secret-key)
    *  [Migrations](#migrations)
    *  [External component configuration](#external-component-configuration)
        *  [Local authentication](#local-authentication)
        *  [Umbrella authentication](#umbrella-authentication)
        *  [Local resource authorization](#local-resource-authorization)
        *  [Dynamic data retrieval](#dynamic-data-retrieval)
    *  [Other relevant application settings](#other-relevant-application-settings)
        *  [Configure resource quotas per user](#configure-resource-quotas-per-user)
        *  [Set the storage root path](#set-the-storage-root-path)
        *  [Set the docker daemon endpoint](#set-the-docker-daemon-endpoint)
    *  [Run](#run)
*  [Testing](#testing)
*  [Deploy](#deploy)
    *  [Configure uswgi](#configure-uswgi)
    *  [Configure Apache](#configure-apache)
---
## Architecture

This backend is built using the [Django](https://www.djangoproject.com/) and [Django REST](https://www.django-rest-framework.org/) frameworks, running over Python 3.6 (Python 3.7 and higher should also be supported). You can refer to the documentation of the respective frameworks for more information.

Additionally, this application is configured to use a MySQL database (versions 5.6 and higher are supported). Other database backends are also supported by the Django framework (PostgreSQL, Oracle, SQLite), but require changes in the settings of the application. Check the relevant [Django documentation](https://docs.djangoproject.com/en/2.0/intro/tutorial02/#database-setup) for further details.

### External components
There are several services with which this backend may interact that are not part of this repository.

#### Guacamole
To connect with the resources (Docker containers, virtual machines...) requisitioned by the application users, this application interfaces with an [Apache Guacamole](https://guacamole.apache.org/) service, which provides VNC or RDP connections through HTTP. 

The only settings required in the backend segment is the connection to the database of your Guacamole instance, which will be used to keep track of the active resources and their access credentials (check the [Database configuration](#database-configuration) section).

#### Local data provider
This application can be configured to retrieve information about the experiments performed in the facility dynamically via a REST API interface from a provider (eg.: a Web User Office application). Check further details in the [Dynamic data retrieval](#dynamic-data-retrieval) section of this document. The interface the provider must implement is documented in the [API.md](API.md) file of this repository.

#### Local authentication provider
This application is designed to interface via a REST API with an existing authentication service of the facility. Check further details in the [Local authentication](#local-authentication) of this document. As before, the interface the provider must implement is documented in the [API.md](API.md) file of this repository.

#### Umbrella

In addition to local authentication schemes implemented in each facility, this application is also designed to provide access via the [Umbrella](https://umbrellaid.org/) federated authentication service. The relevant application settings to enable Umbrella support are detailed in the [Umbrella authentication](#umbrella-authentication) section of this document.
(TODO: Reference to documentation and Shibboleth)

## Requirements

(TODO: detail specs, maybe use a table?)

For a minimal deployment of the backend segment of this application, the following resources are required:

*  An application server to host the Django backend (may also host the frontend application).
*  A database server.
*  A server running the Shibboleth identity provider (required to support the Umbrella federated authentication system).
*  A server running an Apache Guacamole service
*  A server to use as host to the docker containers the users may requisition.

## Build & Development

The project has been developed in Python using Django Framework and the source code can be found in the [Github repository](https://github.com/Calipsoplus/calipsoplus-backend).

The prerequisites for this project is a working installation of Python 3.6+ and pip. The following snippet will clone the repository, set up and enable a Python virtual environment, and install the required dependencies:

```bash
mkdir calipsoplus && cd calipsoplus
mkdir logs
python3 -m venv env
source env/bin/activate
git clone git@github.com:Calipsoplus/calipsoplus-backend.git -b develop backend
pip install -r backend/requirements.txt
```

**N.B.:** Throughout the rest of this readme, we will assume the virtual environment is activated (you should see "(env)" in your shell of choice).

### Database configuration

By default, the application settings are configured to use a MySQL database server, and we need a new schema to manage app's data, with the necessary user and host credentials to manage it. This document will follow default configuration settings.

Create a new database for the application (in mysql shell/IDE):

```sql
CREATE DATABASE `calipsoplus`;
```

And the configuration files for the connections:

```bash
# Assuming we are in the level holding the 'logs' and 'backend' folders...
mkdir config && cd config
mkdir database && cd database
vi default.cnf #calipso db
vi guacamole.cnf #guacamole db
```

Add the following content to the **default.cnf** file to configure the connection to the application database:
```ini
[client]
database = calipsoplus
host = localhost
port = 3306
user = *****
password = *****
default-character-set = utf8
```
Add the following content to the **guacamole.cnf** file to configure the connection to the Apache Guacamole database:
```ini
[client]
database = guacamoledb
host = localhost
port = 3306
user = *****
password = *****
default-character-set = utf8
```

Set **default.cnf** and **guacamole.cnf** files as read only

```bash
chmod 555 default.cnf guacamole.cnf
```

### Environment configuration files
The base configuration settings for the application are specified in the **backend/calipsoplus/settings.py** file. You will want to override part or add to these settings depending on your environment (local development, unit testing, integration, production...), to that end we create environment setting files (eg.: settings_local.py) that will import the main settings file. You can find some example files in the **backend/calipsoplus** folder for reference use.

To use a specific settings file, use the `--settings=calipsoplus.settings_[env]` argument when executing any `manage.py` command.

Note that the .gitignore file of this project is set to ignore any environment setting files (any file matching **backend/calipsoplus/settings__*.py**), so they will not get committed to the repository.

### Secret key
Django uses a variable called "SECRET_KEY" as the basis for its encryption functionality (sessions, cryptographic signing...). This variable should be something long, unique and random. Check the relevant [Django documentation](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECRET_KEY) for more details.

The base settings of the application are already set up to read this value from a configuration file (in **config/secrets/secret_key.cnf**).

### Migrations
Navigate to the **backend** folder. The following command will apply the required migrations to create/update the database schema to the latest version:
```bash
python manage.py migrate --settings=calipsoplus.settings_[local|test|demo|prod]
```

### External component configuration
This section details the settings that need to be modified in order to properly configure connections to the external components described in the [Architecture](#external-components) section.

#### Local authentication
In the **calipsoplus/settings_calypso.py** file, you can set whether local authentication is allowed or not. Set the "ALLOW_LOCAL_AUTHENTICATION" setting to 1 to enable this feature.

The next step to take to configure local authentication is to define the login endpoint. In the **calipsoplus/settings_[local|test|demo|prod].py** file, find the "BACKEND_UO_LOGIN" setting and replace the URL with the endpoint of your provider. This endpoint must implement the expected REST API as described in the [API.md](API.md) file.

#### Umbrella authentication
In order to enable support for the Umbrella federated authentication service, set the relevant endpoints of your Shibboleth identity provider in the **calipsoplus/settings_[local|test|demo|prod].py** file. Two endpoints need to be set: "UMBRELLA_LOGIN" and "UMBRELLA_LOGOUT".

Additionally, an endpoint must be set for a REST service that will authenticate the Umbrella hash against your user records, "BACKEND_UO_HASH". This endpoint must implement the expected REST API as described in the [API.md](API.md) file.

#### Local resource authorization
If the facility provides local resources to users (virtual machines or desktops, independent of experiments performed in the site), you can control the access to these resources via the "BACKEND_UO_IS_AUTHORIZED" endpoint, defined in the **calipsoplus/settings_[local|test|demo|prod].py** file. Check the [API.md](API.md) file for details on the implementation of this endpoint.

This endpoint uses HTTP Basic Authentication as an additional security measure, with credentials set as the **LOCAL_ACCESS_USERNAME** and **LOCAL_ACCESS_PASSWORD** variables in **calipsoplus/settings.py** file.

#### Dynamic data retrieval
This application can be set to dynamically retrieve data of the experiments performed in the site from a REST service. To enable this feature, go to **calipsoplus/settings_calypso.py** and set the "DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL" setting to one.

The endpoint used to retrieve the experiment data is defined in the **calipsoplus/settings_[local|test|demo|prod].py** file as the "DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL_ENDPOINT" setting. This endpoint must implement the expected REST API as described in the [API.md](API.md) file.

This endpoint uses HTTP Basic Authentication as an additional security measure, with credentials set as the **LOCAL_ACCESS_USERNAME** and **LOCAL_ACCESS_PASSWORD** variables in **calipsoplus/settings.py** file.

### Other relevant application settings
#### Configure resource quotas per user
To configure the resource quotas to which users are limited, modify the relevant settings in the **calipsoplus/settings_calipso.py** file. Currently, you can set the maximum number of containers, and total RAM, CPU, and Storage a user is allowed to requisition.

#### Set the storage root path
Paths to the datasets of an experiment are built dynamically, but the root path to the storage mounting needs to be defined in the **calipsoplus/settings_calipso.py** file. Use "EXPERIMENTS_DATASETS_ROOT" for datasets that will be mounted in "read-only" mode, and "EXPERIMENTS_OUTPUT" for the results of operations performed in the requisitioned resource.

#### Set the docker daemon endpoint
In order to requisition new docker containers, the application has to communicate with an existing Docker daemon. The endpoints to contact with this service are set in the relevant settings.py file (eg.: settings_local.py). There are two variables that need to be set:
*  **DOCKER_URL_DAEMON**: takes the form of "tcp://MACHINE_IP:DOCKER_PORT", where "MACHINE_IP" is the IP of the machine that hosts the Docker daemon and "DOCKER_PORT" is the port the daemon is listening to.
*  **REMOTE_MACHINE_IP**: the IP of the mchine that hosts the Docker daemon.

### Run

Once the environment and the database are configured...

```bash
python manage.py runserver 127.0.0.1:8000 settings=calipsoplus.settings_local
```

The service should be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Testing

The application has its own unit testing settings, which will create a mock database using SQLite and will store it in local memory. This way the testing is faster than using MySQL.

```bash
python manage.py test --settings=calipsoplus.settings_unittests
```

## Deploy

Follow the same steps as in the **Build & Development** section except the **Run** subsection.

### Configure uswgi

Go to uwsgi's directory which contains the apps-available and apps-enabled directories. We will name it UWSGI_DIR.

Create a new .ini file, **calipsoPlus.ini** in the apps-available folder, an example of the configuration file would be as follows:
```ini
[uwsgi]
socket = 127.0.0.1:{PORT}
master=True
chdir={CALIPSO_BACKEND_FOLDER}
module=calipsoplus.wsgi:application
home={VIRTUAL_ENV_FOLDER}
logger = file:{CALIPSO_UWSGI_LOG_LOCATION}
pidfile = {CALIPSO_UWSGI_PID_FILE}
stats = /tmp/calipsoplus-stats
touch-reload = {RELOAD_FILE}
env = DJANGO_SETTINGS_MODULE={ENVIRONMENT_SETTINGS_FILE}
processes = 4
threads = 2
```
Replace the placeholders with the following:
*  **PORT**: Port to which UWSGI will map the application (you can proxy this later with an Apache frontend)
*  **CALIPSO_BACKEND_FOLDER**: Folder which contains the **manage.py** file of the backend.
*  **VIRTUAL_ENV_FOLDER**: Location of the Python virtual environment used for the application.
*  **CALIPSO_UWSGI_LOG_LOCATION**: Location where you want to save the UWSGI request logs.
*  **CALIPSO_UWSGI_PID_FILE**: Location where the application PID file will be saved (this is usually UWSGI_DIR/config/pid/calipsoplus.pid).
*  **RELOAD_FILE**: A file UWSGI watches for changes to trigger a hot reload of the application (usually we use the README of the application).
*  **ENVIRONMENT_SETTINGS_FILE**: The settings file used for this deployment, one of **settings_[test|demo|prod]** (depending on which environment you are deploying).

Once you are sure the values are correct, sym-link it to the apps-enabled folder and restart the UWSGI service.

### Configure Apache

Go to Apache's directory which contains the **apps-available** and **apps-enabled** directories, we will name it APACHE_DIR. SOURCE_DIR is the folder containing the **manage.py** file.

```bash
cd APACHE_DIR/apps-available
cp SOURCE_DIR/calipsoplus/config/apache/calipsoplus-backend.conf .
cd ../apps-enabled
ln -s ../apps-available/calipsoplus-backend.conf XX-calipsoplus-backend.conf
```

Modify the file as needed to point to the locations and WSGI port of your project. When you are done, reload the configuration files:

```bash
sudo service apache2 reload
```