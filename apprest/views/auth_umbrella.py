import json
import logging

import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status


class ExternalUmbrellaServiceAuthenticationBackend:
    logger = logging.getLogger(__name__)

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

    def authenticate(self, request, uid=None, eaa_hash=None):
        self.logger.info('Attempting to authenticate via umbrella')
        try:
            if None in (uid, eaa_hash):
                self.logger.warning('Tried to authenticate user with missing fields, rejecting')
                return None

            post_data = {'uid': uid, 'EAAHash': eaa_hash}

            headers = {'Content-type': 'application/json'}
            response = requests.post(settings.BACKEND_UO_HASH,
                                     data=json.dumps(post_data),
                                     headers=headers, verify=False)

            if response.status_code == status.HTTP_200_OK:
                self.logger.info('Authenticated %s', uid)
                try:
                    user = User.objects.get(username=uid)
                    return user
                except User.DoesNotExist as udne:
                    self.logger.info('Creating %s user in django database, as it is not yet present', uid)
                    # User will have unusable password, it is authenticated externally
                    user = User.objects.create_user(uid, '')
                    user.save()
                    return user
            return None
        except Exception as e:
            self.logger.debug(e)