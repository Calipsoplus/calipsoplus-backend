from django.utils.timezone import now
from rest_framework.test import APITestCase

import logging

from apprest.models import CalipsoSession
from apprest.models.experiment import CalipsoExperiment
from apprest.services.session import CalipsoSessionsServices

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

        self.service.create_session_to_experiment(session_number="SS_1", start_date='2017-06-08T00:01:00',end_date='2017-06-08T00:01:20',subject="SUBJECT SESSION 1", body="BODY SESSION 1",
                                                  data_set_path="/path/other_path/", experiment=experiment_3)

        self.service.create_session_to_experiment(session_number="SS_2", start_date='2017-06-08T00:01:00',end_date='2017-06-08T00:01:20', subject="SUBJECT SESSION 2",
                                                  body="BODY SESSION 2",
                                                  data_set_path="/path/other_path/", experiment=experiment_3)

        self.service.create_session_to_experiment(session_number="SS_3", start_date='2017-06-08T00:01:00',end_date='2017-06-08T00:01:20', subject="SUBJECT SESSION 3",
                                                  body="BODY SESSION 3",
                                                  data_set_path="/path/other_path/", experiment=experiment_3)

        sessions = self.service.get_sessions_from_experiment(experiment_3)
        self.assertEqual(len(sessions), 3)

        self.logger.debug('#### TEST test_add_3_sessions_to_one_experiment END ####')

    def test_add_session_to_one_experiment(self):
        self.logger.debug('#### TEST test_add_session_to_one_experiment START ####')

        experiment_2 = CalipsoExperiment.objects.get(pk=2)

        self.service.create_session_to_experiment(session_number="SS_1", start_date='2017-06-08T00:01:00',end_date='2017-06-08T00:01:20', subject="SUBJECT SESSION 1",
                                                  body="BODY SESSION 1",
                                                  data_set_path="/path/other_path/", experiment=experiment_2)

        sessions = self.service.get_sessions_from_experiment(experiment_2)
        self.assertEqual(len(sessions), 2)

        self.logger.debug('#### TEST test_add_session_to_one_experiment END ####')