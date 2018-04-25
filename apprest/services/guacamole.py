import hashlib
import logging
import random
import pdb
from django.utils import timezone

from cffi.backend_ctypes import xrange

from apprest.models.guacamole import GuacamoleUser, GuacamoleConnection, GuacamoleConnectionPermission, \
    GuacamoleConnectionParameter


class CalipsoGuacamoleServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_connection(self, username, password, connection_name, protocol, vncpassword, ip, port):
        self.logger.info('Attempting to run create_connection')

        try:
            salt = bytearray(random.getrandbits(8) for _ in xrange(32))
            salt_hex = ''.join('{:02X}'.format(x) for x in salt)
            password_hash = hashlib.sha256((password + salt_hex).encode('utf-8)')).digest()

            # delete guacamole user
            GuacamoleUser.objects.using('guacamole').filter(username=username).delete()

            # create new connection
            connection = GuacamoleConnection.objects.using('guacamole').create(connection_name=connection_name,
                                                                               protocol=protocol, failover_only=0)

            user = GuacamoleUser.objects.using('guacamole').create(username=username, password_salt=salt,
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
                parameter_value=ip)

            GuacamoleConnectionParameter.objects.using('guacamole').create(
                connection=connection,
                parameter_name="port",
                parameter_value=port)

            GuacamoleConnectionParameter.objects.using('guacamole').create(
                connection=connection,
                parameter_name="password",
                parameter_value=vncpassword)

            return "ok"

        except Exception as e:
            pdb.set_trace()
            return e



