import logging

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

    def get_all_users(self, request):
        return CalipsoUser.objects.all()
