import logging

from rest_framework.exceptions import NotFound

from apprest.models import CalipsoUser
from calipsoplus.settings_calipso import ENABLE_NON_ROOT_UID_CONTAINER, ENABLE_NON_ROOT_GID_CONTAINER, \
    ADD_HOME_DIR_TO_ALL_CONTAINERS


class CalipsoUserServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_umbrella_session_hash(self, request):
        self.logger.debug('try to get umbrella session')
        try:
            #session_hash = request.META["HTTP_EAAHASH"]
            session_hash = request.META["EAAHash"]
            #uid = request.META["HTTP_UID"]
            uid = request.META["uid"]

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

    def get_user_uid(self, username):
        """Returns a user's UID
        This method needs to be implemented by each site so that it looks up the UID.
        If this setting is disabled, returns 0 which is the UID for root.
        :param username:
        :return: UID in the form of an integer.
        """
        if ENABLE_NON_ROOT_UID_CONTAINER:
            if username is not None:
                return 0  # Change this to return the correct UID
            return 0
        # if the method is not implemented or if the username is set to None, root uid will be returned
        return 0

    def get_user_gid(self, username):
        """Returns a user's GID
        This method needs to be implemented by each site so that it looks up the GID.
        If this setting is disabled, returns 0 which is the GID for root.
        :param username:
        :return: GID in the form of an integer.
        """
        if ENABLE_NON_ROOT_GID_CONTAINER:
            if username is not None:
                return 0  # Change this to return the correct GID
            return 0
        # if the method is not implemented or if the username is set to None, root gid will be returned
        return 0

    def get_user_home_dir(self, username):
        """Returns the path to the user's home directory (NFS host path)
        This method needs to be implemented by each site so that it looks up the path.
        :param username:
        :return: Home directory path in the form of a string
        """
        if username is not None:
            return None  # # Change this to return the correct path
        return None
