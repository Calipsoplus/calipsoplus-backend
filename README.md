# CalipsoPlus Backend

The aim of this project is to provide a backend RESTful service for CELLS' CalipsoPlus project.

## Build & Development

The project has been developed in Python using Django Framework and the source code can be found in [CELLS' Git repository](https://git.cells.es/mis/calipsoplus-backend).

The user will need to install Python 3+, python-pip and python-virtualenv. Some other packages could be required.

```bash
mkdir calipsoplus & cd calipsoplus
mkdir logs
virtualenv ~/.virtualenvs/calipsoenv/bin/activate
git clone https://github.com/Calipsoplus/calipsoplus-backend.git -b develop backend
env/bin/pip install -r calipsoplus/requirements.txt
```

### Database configuration

By default, the application settings are configured to use MySQL database server, and we need a new schema to manage app's data, with the necessary user and host credentials to manage it. This document will follow default configuration settings.

```sql
CREATE DATABASE `calipsoplus`;
```

```bash
cd calipsoplus
mkdir config & cd config
mkdir database & cd database
vi guacamole.cnf #guacamole db
vi default.cnf #calipso db
```

Add the following content to the **default.cnf** file
```bash
[client]
database = calipsoplus
host = localhost
port = 3306
user = *****
password = *****
default-character-set = utf8
```
Add the following content to the **guacamole.cnf** file
```bash
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
chmod 555 default.cnf
chmod 555 guacamole.cnf
```

### Migrate
```
env/bin/python backend/manage.py migrate --settings=calipsoplus.settings_[local|test|demo|prod]
```

### Run

Once the environment and the database are configured...

```bash
python manage.py runserver 127.0.0.1:8000 --settings=calipsoplus.settings_local
```

The service should be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Testing

The application has its own unit testing settings, which will create a mock database using SQLite and will store it in local memory. This way the testing is faster than using MySQL.

```bash
cd calipsoplus
source ~/.virtualenvs/calipsoenv/bin/activate
./manage.py test --settings=calipsoplus.settings_unittests
```

## Deploy

Follow the same steps as in the **Build & Development** section except the **Run** subsection

### Configure uswgi

Go to uwsgi's directory which contains the apps-available and apps-enabled directories. We will name it UWSGI_DIR.

First of all, review the calipsoplus-backend.ini file to be sure every property is set correctly.

After that, we need to edit the configuration file with correct environment configuration in terms of project location, Django's environment settings and database configuration.

### Configure Apache

Go to Apache's directory which contains the apps-available and apps-enabled directories. We will name it APACHE_DIR.

```bash
cd APACHE_DIR/apps-available
cp SOURCE_DIR/settings/config/apache/calipsoplus-backend.conf .
cd ../apps-enabled
ln -s ../apps-available/calipsoplus-backend.conf XX-calipsoplus-backend.conf
```

### Restart the service

```bash
sudo service apache2 restart
```
