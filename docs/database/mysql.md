# MySQL config

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'read_default_file': os.path.join(BASE_DIR, '..', 'config', 'database', 'default.cnf'),
        }
    },
    'guacamole': {
        'ENGINE': 'django.db.backends.mysql',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'read_default_file': os.path.join(BASE_DIR, '..', 'config', 'database', 'guacamole.cnf'),
        },
    },
}
```
