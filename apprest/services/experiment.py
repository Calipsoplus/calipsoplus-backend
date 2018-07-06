import logging

from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound

from apprest.models.user import CalipsoUser


class CalipsoExperimentsServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_user_experiments(self, username):
        self.logger.debug('Getting get_user_experiments from user_id %s', username)
        try:
            user = User.objects.get(username=username)
            experiments = CalipsoUser.objects.get(user=user).experiments.all()
            return experiments
        except User.DoesNotExist as dne:
            self.logger.debug(dne)
            raise NotFound(detail='User not found')
        except Exception as e:
            self.logger.debug(e)
            raise e