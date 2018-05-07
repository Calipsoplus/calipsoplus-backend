import logging

from apprest.models.user import CalipsoUser


class CalipsoExperimentsServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_user_experiments(self, user_id):
        self.logger.debug('Getting get_user_experiments from user_id %s', user_id)
        try:
            experiments = CalipsoUser.objects.get(user_id=user_id).experiments.all()
            self.logger.debug('get_user_experiments got')
            return experiments
        except Exception as e:
            self.logger.error(e)
            raise e


