import json

from django.utils.timezone import now
from rest_framework.test import APITestCase

import logging

from apprest.models.experiment import CalipsoExperiment
from apprest.services.session import CalipsoSessionsServices
from calipsoplus.settings_calipso import EXPERIMENTS_DATASETS_ROOT, EXPERIMENTS_OUTPUT

logger = logging.getLogger(__name__)


class SessionServiceTestCase(APITestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['users.json', 'experiments.json', 'sessions.json']

    def setUp(self):
        self.logger.debug('#### setUp SessionServiceTestCase START ####')
        self.service = CalipsoSessionsServices()
        self.logger.debug('#### setUp SessionServiceTestCase END ####')

    def test_default_sessions(self):
        self.logger.debug('#### TEST test_default_sessions START ####')

        experiment_1 = CalipsoExperiment.objects.get(pk=1)

        sessions = self.service.get_sessions_from_experiment(experiment_1)
        self.assertEqual(len(sessions), 2)

        experiment_2 = CalipsoExperiment.objects.get(pk=2)

        sessions = self.service.get_sessions_from_experiment(experiment_2)
        self.assertEqual(len(sessions), 1)

        experiment_3 = CalipsoExperiment.objects.get(pk=3)

        sessions = self.service.get_sessions_from_experiment(experiment_3)
        self.assertEqual(len(sessions), 0)

        self.logger.debug('#### TEST test_default_sessions END ####')

    def test_add_3_sessions_to_one_experiment(self):
        self.logger.debug('#### TEST test_add_3_sessions_to_one_experiment START ####')

        experiment_3 = CalipsoExperiment.objects.get(pk=3)

        params = {'session_number': "SS_1",
                  'start_date': "2017-06-08T00:01:00",
                  'end_date': "2017-07-08T00:01:00",
                  'subject': "SUBJECT SESSION 1",
                  'body': "BODY SESSION 1",
                  'data_set_path': "{'/var/www/': {'bind': '/mnt/www', 'mode': 'rw'},'/var/log': {'bind': '/mnt/log', 'mode': 'ro'}}"}

        self.service.create_session_to_experiment(params=params, experiment=experiment_3)

        params = {'session_number': "SS_2",
                  'start_date': "2017-06-08T00:01:00",
                  'end_date': "2017-07-08T00:01:00",
                  'subject': "SUBJECT SESSION 2",
                  'body': "BODY SESSION 2",
                  'data_set_path': "{'/var/www/': {'bind': '/mnt/www', 'mode': 'rw'},'/var/log': {'bind': '/mnt/log', 'mode': 'ro'}}"}

        self.service.create_session_to_experiment(params=params, experiment=experiment_3)

        params = {'session_number': "SS_3",
                  'start_date': "2017-06-08T00:01:00",
                  'end_date': "2017-07-08T00:01:00",
                  'subject': "SUBJECT SESSION 3",
                  'body': "BODY SESSION 3",
                  'data_set_path': "{'/var/www/': {'bind': '/mnt/www', 'mode': 'rw'},'/var/log': {'bind': '/mnt/log', 'mode': 'ro'}}"}

        self.service.create_session_to_experiment(params=params, experiment=experiment_3)

        sessions = self.service.get_sessions_from_experiment(experiment_3)
        self.assertEqual(len(sessions), 3)

        self.logger.debug('#### TEST test_add_3_sessions_to_one_experiment END ####')

    def test_add_session_to_one_experiment(self):
        self.logger.debug('#### TEST test_add_session_to_one_experiment START ####')

        experiment_2 = CalipsoExperiment.objects.get(pk=2)

        params = {'session_number': "SS_1",
                  'start_date': "2017-06-08T00:01:00",
                  'end_date': "2017-07-08T00:01:00",
                  'subject': "SUBJECT SESSION 1",
                  'body': "BODY SESSION 1",
                  'data_set_path': "{'/var/www/': {'bind': '/mnt/www', 'mode': 'rw'},'/var/log': {'bind': '/mnt/log', 'mode': 'ro'}}"}

        self.service.create_session_to_experiment(params=params, experiment=experiment_2)

        sessions = self.service.get_sessions_from_experiment(experiment_2)
        self.assertEqual(len(sessions), 2)

        self.logger.debug('#### TEST test_add_session_to_one_experiment END ####')

    def test_volumes_session(self):
        self.logger.debug('#### TEST test_volumes_session START ####')

        experiment_2 = CalipsoExperiment.objects.get(pk=2)

        params = {'session_number': "SS_1",
                  'start_date': "2017-06-08T00:01:00",
                  'end_date': "2017-07-08T00:01:00",
                  'subject': "SUBJECT SESSION 1",
                  'body': "BODY SESSION 1",
                  'data_set_path': "{'/var/www/': {'bind': '/mnt/www', 'mode': 'rw'},'/var/log': {'bind': '/mnt/log', 'mode': 'ro'}}"}

        self.service.create_session_to_experiment(params=params, experiment=experiment_2)

        volumes = self.service.get_volumes_from_session(session_number='SS_1')

        ro = ""
        rw = ""
        for volume in volumes.keys():
            if volumes[volume]['mode'] == 'ro':
                ro = volumes[volume]['bind']
            if volumes[volume]['mode'] == 'rw':
                rw = volumes[volume]['bind']

        self.assertTrue(ro.__contains__(EXPERIMENTS_DATASETS_ROOT))
        self.assertTrue(rw.__contains__(EXPERIMENTS_OUTPUT))

        self.logger.debug('#### TEST test_volumes_session END ####')
