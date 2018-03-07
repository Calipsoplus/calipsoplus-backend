import logging

from apprest.models.user import CalipsoUser


class CalipsoUserServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all_users(self):
        self.logger.debug('Getting all application users')
        try:
            all_users = CalipsoUser.objects.all()
            self.logger.debug('All application users got')
            return all_users
        except Exception as e:
            self.logger.error(e)
            raise e

    def get_user(self, user_id):
        self.logger.debug('Getting user %s', user_id)
        try:
            user = CalipsoUser.objects.get(user_id = user_id)
            self.logger.debug('User got')
            return user
        except Exception as e:
            self.logger.error(e)
            raise e

    def get_user_experiments(self, user_id):
        self.logger.debug('Getting get_user_experiments from user_id %s', user_id)
        try:
            experiments = CalipsoUser.objects.get(user_id=user_id).experiments.all()
            self.logger.debug('get_user_experiments got')
            return experiments
        except Exception as e:
            self.logger.error(e)
            raise e