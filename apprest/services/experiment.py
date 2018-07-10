import logging

from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound

from apprest.models.experiment import CalipsoExperiment
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

    def add_user_to_experiment(self, username, experiment):
        self.logger.debug('Adding user: %s to experiment: %s' % (username, experiment))
        user = User.objects.get(username=username)
        calipso_user = CalipsoUser.objects.get(user=user)
        experiment = CalipsoExperiment.objects.get(serial_number=experiment)
        calipso_user.experiments.add(experiment)
        calipso_user.save()

    def add_experiment(self, beamline_code, description, public_number, title):
        self.logger.debug('Try to add experiment %s' % public_number)
        calipso_experiment = CalipsoExperiment.objects.filter(serial_number=public_number)
        if len(calipso_experiment) > 0:
            raise Exception('Experiment already exists.')
        else:
            calipso_experiment = CalipsoExperiment()
            calipso_experiment.subject = title
            calipso_experiment.serial_number = public_number
            calipso_experiment.body = description
            calipso_experiment.beam_line = beamline_code

            calipso_experiment.save()

    def remove_experiment(self, public_number):
        self.logger.debug('Try to remove experiment %s' % public_number)
        CalipsoExperiment.objects.get(serial_number=public_number).delete()

    def remove_user_from_experiment(self, username, public_number):
        self.logger.debug('Try to remove user %s from experiment %s' % (username,public_number))
        user = User.objects.get(username=username)
        calipso_user = CalipsoUser.objects.get(user=user)
        calipso_experiment = CalipsoExperiment.objects.get(serial_number=public_number)
        calipso_user.experiments.remove(calipso_experiment)
        calipso_user.save()

    def update_experiment(self, beamline_code, description, public_number, title):
        self.logger.debug('Try to update experiment %s' % public_number)
        calipso_experiment = CalipsoExperiment.objects.get(serial_number=public_number)
        if title:
            calipso_experiment.subject = title
        if description:
            calipso_experiment.body = description
        if beamline_code:
            calipso_experiment.beam_line = beamline_code
        calipso_experiment.save()