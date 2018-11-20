import hashlib
import logging
import random

from django.utils import timezone

from cffi.backend_ctypes import xrange

from apprest.models.guacamole import GuacamoleUser, GuacamoleConnection, GuacamoleConnectionPermission, \
    GuacamoleConnectionParameter


class CalipsoGuacamoleServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_connection(self, params):
        self.logger.info('Attempting to run create_connection_guacamole')

        guacamole_username=params["guacamole_username"]
        guacamole_password=params["guacamole_password"]
        guacamole_connection_name=params["guacamole_connection_name"]
        guacamole_protocol=params["guacamole_protocol"]
        vnc_password=params["vnc_password"]
        container_ip=params["container_ip"]
        container_port=params["container_port"]

        try:
            salt = bytearray(random.getrandbits(8) for _ in xrange(32))
            salt_hex = ''.join('{:02X}'.format(x) for x in salt)
            password_hash = hashlib.sha256((guacamole_password + salt_hex).encode('utf-8)')).digest()

            # delete guacamole user
            GuacamoleUser.objects.using('guacamole').filter(username=guacamole_username).delete()

            # create new connection
            connection = GuacamoleConnection.objects.using('guacamole').create(
                connection_name=guacamole_connection_name,
                protocol=guacamole_protocol, failover_only=0)

            user = GuacamoleUser.objects.using('guacamole').create(username=guacamole_username, password_salt=salt,
                                                                   password_hash=password_hash,
                                                                   password_date=timezone.now(),
                                                                   disabled=0,
                                                                   expired=0)

            GuacamoleConnectionPermission.objects.using('guacamole').create(user=user,
                                                                            connection=connection,
                                                                            permission='READ')

            GuacamoleConnectionParameter.objects.using('guacamole').create(
                connection=connection,
                parameter_name="hostname",
                parameter_value=container_ip)

            GuacamoleConnectionParameter.objects.using('guacamole').create(
                connection=connection,
                parameter_name="port",
                parameter_value=container_port)

            GuacamoleConnectionParameter.objects.using('guacamole').create(
                connection=connection,
                parameter_name="password",
                parameter_value=vnc_password)

            return "ok"

        except Exception as e:
            return e
