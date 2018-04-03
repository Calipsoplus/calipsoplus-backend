from django.conf import settings
import hashlib
import logging
# from django.contrib.auth.hashers

from calipsoplus.auth.models import User, AuthDatabaseUser

class ExternalDatabaseAuthenticationBackend:
    logger = logging.getLogger(__name__)

    def authenticate(self, request, username=None, password=None):
        self.logger.info('Attempting to authenticate via auth_db')
        try:
            if None in (username, password):
                self.logger.warning('Tried to authenticate user with missing fields, rejecting')
                return None

            # Fetch user from auth_db
            self.logger.debug('Authenticating %s', username)
            try:
                auth_user = AuthDatabaseUser.objects.get(login=username)
            except AuthDatabaseUser.DoesNotExist:
                log.info('%s not found in auth_db', username)
                return None

            # Hash password
            hash = hashlib.md5()
            hash.update(password.encode('utf-8'))
            hashed_pass = hash.hexdigest()

            # Check match
            if hashed_pass == auth_user.password:
                self.logger.info('Authenticated %s', username)
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist as dne:
                    self.logger.info('Creating %s user in django database, as it is not yet present', username)
                    # User will have unusable password, it is authenticated externally
                    user = User.objects.create_user(username,'')
                    user.save()
                return user
            return None

        except Exception as e:
            self.logger.error(e)
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
