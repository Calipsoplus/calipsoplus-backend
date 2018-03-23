from django.conf import settings
import hashlib
import logging
# from django.contrib.auth.hashers

from django.
from calipsoplus.auth.models import User, AuthDatabaseUser

class DatabaseAuthenticationBackend:
    self.logger = logging.getLogger(__name__)

    def authenticate(self, request, username=None, password=None):
        logger.info('Attempting to authenticate via auth_db')
        try:
            if None in (username, password):
                logger.warning('Tried to authenticate user with missing fields, rejecting')
                return None

            # Fetch user from auth_db
            logger.debug('Authenticating %s', username)
            try:
                auth_user = AuthDatabaseUser.objects.get(login=username)
            except AuthDatabaseUser.DoesNotExist:
                log.info('%s not found in auth_db', username)
                return None

            # Hash password
            hash = hashlib.md5()
            hash.update(password.encode('utf-8'))
            hashed_pass = hash.digest()
            if hashed_pass == auth_user:
                logger.debug('Authenticated %s', username)
                return User.objects.get(login=username)
            return None

        except Exception as e:
            logger.error(e)
            raise e

    def get_user(self, user_id):
        """
        Retrieve the user's entry in the User model if it exists
        :param user_id:
        :return:
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
