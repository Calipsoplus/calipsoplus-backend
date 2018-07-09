import logging
from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class UpdateExperimentCommandTest(TestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

    def test_command_update_existent_experiment(self):
        out = StringIO()

        call_command('update_experiment', '--public_number=2018091632', "--set_title =new title",
                     "--set_description = new description", "--set_beamline-code = new beamline code", stdout=out)

        self.assertIn("Successfully updated experiment", out.getvalue())

    def test_command_update_non_existent_experiment(self):
        out = StringIO()

        with self.assertRaises(Exception):
            call_command('update_experiment', '--public_number=218091632', "--set_title =new title",
                         "--set_description = new description", "--set_beamline-code = new beamline code", stdout=out)