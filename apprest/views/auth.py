import hashlib
import json
import logging
import pdb

import requests
from django.contrib.auth.models import User
from rest_framework import status

from apprest.models.auth import AuthDatabaseUser
from calipsoplus.settings import BACKEND_UO


class ExternalDatabaseAuthenticationBackend:
    logger = logging.getLogger(__name__)

    def authenticate(self, request, username=None, password=None):
        self.logger.info('Attempting to authenticate via auth_db')

        try:
            if None in (username, password):
                self.logger.warning('Tried to authenticate user with missing fields, rejecting')
                return None

            post_data = {'username': username, 'password': password}
            headers = {'Content-type': 'application/json'}
            response = requests.post(BACKEND_UO, data=json.dumps(post_data), headers=headers)

            if response.status_code == status.HTTP_200_OK:
                self.logger.info('Authenticated %s', username)
                try:
                    user = User.objects.get(username=username)
                    return user
                except User.DoesNotExist as udne:
                    self.logger.info('Creating %s user in django database, as it is not yet present', username)
                    # User will have unusable password, it is authenticated externally
                    user = User.objects.create_user(username, '')
                    user.save()
                    return user
            return None
        except Exception as e:
            self.logger.error(e)
            return None


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