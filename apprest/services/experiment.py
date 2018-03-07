import logging

from apprest.models.experiments import CalipsoExperiment




class CalipsoExperimentsServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_experiment(self, experiment_id):
        self.logger.debug('Getting experiment %s', experiment_id)
        try:
            experiment = CalipsoExperiment.objects.get(id=experiment_id)
            self.logger.debug('Experiment %s', experiment_id)
            return experiment
        except Exception as e:
            self.logger.error(e)
            raise e

    def get_all_experiments(self):
        self.logger.debug('Getting all experiments')
        try:
            experiments = CalipsoExperiment.objects.all()
            self.logger.debug('All application experiments got')
            return experiments
        except Exception as e:
            self.logger.error(e)
            raise e
