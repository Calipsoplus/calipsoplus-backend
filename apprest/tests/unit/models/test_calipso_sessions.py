from apprest.plugins.icat.models.calipso_session import CalipsoSession
from django.test import TestCase

import json
import datetime
from apprest.plugins.icat.helpers.complex_encoder import ComplexEncoder


class CalipsoExperimentModelTest(TestCase):

    def test_object_creation(self):
        calipso_session = CalipsoSession(1)
        self.assertEqual(calipso_session.session_number, 1)
        self.assertEqual(calipso_session.subject, '')
        self.assertEqual(calipso_session.body, '')
        self.assertEqual(calipso_session.end_date, '')
        self.assertEqual(calipso_session.start_date, '')

    def test_json_representation(self):
        calipso_session = CalipsoSession(1)
        calipso_session.body = 'This is the body'
        calipso_session.subject = 'This is the subject'
        calipso_session.start_date = datetime.datetime(2019, 4, 29, 11, 42, 0, 243509)
        calipso_session.start_date = datetime.datetime(2019, 4, 30, 11, 00, 0, 243509)
        calipso_session_json = json.dumps(calipso_session, cls=ComplexEncoder, sort_keys=True)

        self.assertEqual(calipso_session_json, '{"body": "This is the body", "data_set_path": "", "end_date": "", '
                                               '"session_number": 1, "start_date": "2019-04-30T11:00:00.243509", '
                                               '"subject": "This is the subject"}')
