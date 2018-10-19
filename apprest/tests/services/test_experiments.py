from rest_framework.test import APITestCase

import logging

from apprest.models.experiment import CalipsoExperiment
from apprest.models.user import CalipsoUser
from apprest.services.experiment import CalipsoExperimentsServices

logger = logging.getLogger(__name__)


class ExperimentServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['users.json', 'experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp ExperimentServiceTestCase START ####')
        self.service = CalipsoExperimentsServices()
        self.logger.debug('#### setUp ExperimentServiceTestCase END ####')

    def test_add_two_experiments_to_user(self):
        self.logger.debug('#### TEST test_add_two_experiments_to_user START ####')

        calipso_user = CalipsoUser.objects.get(pk=1)
        experiment_1 = CalipsoExperiment.objects.get(pk=1)
        experiment_2 = CalipsoExperiment.objects.get(pk=2)

        self.service.add_user_to_experiment(username=calipso_user.user.username,
                                            public_number=experiment_1.serial_number)

        self.service.add_user_to_experiment(username=calipso_user.user.username,
                                            public_number=experiment_2.serial_number)

        experiments = self.service.get_user_experiments(calipso_user.user.username)
        self.assertEqual(len(experiments), 2)

        self.logger.debug('#### TEST test_add_two_experiments_to_user END ####')

    def test_remove_user_from_experiment(self):
        self.logger.debug('#### TEST test_remove_user_from_experiment START ####')

        calipso_user = CalipsoUser.objects.get(pk=1)
        experiment_1 = CalipsoExperiment.objects.get(pk=1)
        experiment_2 = CalipsoExperiment.objects.get(pk=2)

        self.service.add_user_to_experiment(username=calipso_user.user.username,
                                            public_number=experiment_1.serial_number)

        self.service.add_user_to_experiment(username=calipso_user.user.username,
                                            public_number=experiment_2.serial_number)

        self.service.remove_user_from_experiment(username=calipso_user.user.username,
                                                 public_number=experiment_1.serial_number)

        self.service.remove_user_from_experiment(username=calipso_user.user.username,
                                                 public_number=experiment_2.serial_number)

        experiments = self.service.get_user_experiments(calipso_user.user.username)
        self.assertEqual(len(experiments), 0)

        self.logger.debug('#### TEST test_remove_user_from_experiment END ####')

    def test_update_title_experiment(self):
        self.logger.debug('#### TEST test_update_title_experiment START ####')

        experiment_1 = CalipsoExperiment.objects.get(pk=1)

        self.assertEqual(experiment_1.subject, "Experiment 1")

        self.service.update_experiment(beamline_code=experiment_1.beam_line, description=experiment_1.body,
                                       public_number=experiment_1.serial_number, title="Experiment A")

        experiment = CalipsoExperiment.objects.get(pk=1)

        self.assertEqual(experiment.subject, "Experiment A")

        self.logger.debug('#### TEST test_update_title_experiment END ####')

    def test_update_description_experiment(self):
        self.logger.debug('#### TEST test_update_description_experiment START ####')

        experiment_1 = CalipsoExperiment.objects.get(pk=1)

        self.assertEqual(experiment_1.body, "Description of experiment 1")

        self.service.update_experiment(beamline_code=experiment_1.beam_line, description="New description",
                                       public_number=experiment_1.serial_number, title=experiment_1.subject)

        experiment = CalipsoExperiment.objects.get(pk=1)

        self.assertEqual(experiment.body, "New description")

        self.logger.debug('#### TEST test_update_description_experiment END ####')



