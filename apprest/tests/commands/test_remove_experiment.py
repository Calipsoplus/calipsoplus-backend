import logging
from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class RemoveExperimentCommandTest(TestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

    def test_command_remove_one_experiment(self):
        out = StringIO()

        call_command('remove_experiment', '--public_number=2018091632', stdout=out)
        self.assertIn("Successfully removed experiment", out.getvalue())

    def test_command_remove_nonexistent_experiment(self):
        out = StringIO()

        with self.assertRaises(Exception):
            call_command('remove_experiment', '--public_number=XXXX', stdout=out)


