from apprest.plugins.icat.models.calipso_experiment import CalipsoExperiment
from django.test import TestCase

import json
from apprest.plugins.icat.helpers.complex_encoder import ComplexEncoder


class CalipsoExperimentModelTest(TestCase):

    def test_object_creation(self):
        calipso_experiment = CalipsoExperiment(1)
        self.assertEqual(calipso_experiment.proposal_id, 1)
        self.assertEqual(calipso_experiment.sessions, [])
        self.assertEqual(calipso_experiment.beam_line, [])
        self.assertEqual(calipso_experiment.subject, '')
        self.assertEqual(calipso_experiment.gid, None)
        self.assertEqual(calipso_experiment.uid, None)

        calipso_experiment.body = 'This is the body'
        calipso_experiment.subject = 'This is the subject'
        calipso_experiment.beam_line = 'BM-18'

    def test_json_representation(self):
        calipso_experiment = CalipsoExperiment(1)
        calipso_experiment.body = 'This is the body'
        calipso_experiment.subject = 'This is the subject'
        calipso_experiment.beam_line = ['BM-18']
        calipso_experiment_json = json.dumps(calipso_experiment, cls=ComplexEncoder, sort_keys=True)

        self.assertEqual(calipso_experiment_json, '{"beam_line": ["BM-18"], "body": "This is the body", "gid": null, '
                                                  '"proposal_id": 1, "sessions": [], "subject": "This is the '
                                                  'subject", "uid": null}')


