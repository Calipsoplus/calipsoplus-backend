import logging

from rest_framework.exceptions import NotFound

from apprest.models import CalipsoUser


class CalipsoUserServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_umbrella_session_hash(self, request):
        self.logger.debug('try to get umbrella session')
        try:
            session_hash = request.META["HTTP_EAAHASH"]
            uid = request.META["HTTP_UID"]

            json_session_data = {'EAAHash': session_hash, 'uid': uid}

            self.logger.debug('umbrella session got it')
            return json_session_data

        except KeyError:
            return None

    def get_all_users(self):
        self.logger.debug("Attempting to retrieve all users")
        try:
            users = CalipsoUser.objects.all()
            self.logger.debug("Retrieved all users")
            return users
        except Exception as e:
            self.logger.error(e)
            raise Exception

    def get_user(self, username):
        self.logger.debug('Getting user profile: %s' % username)
        try:
            user = CalipsoUser.objects.get(user__username=username)
            self.logger.debug('User found')
            return user

        except Exception as e:
            self.logger.error("%s not found." % username)
            self.logger.error(e)
            raise NotFound
