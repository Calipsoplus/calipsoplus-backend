import logging
from io import StringIO
from django.core.management import call_command
from django.test import TestCase

logger = logging.getLogger(__name__)


class AddExperimentCommandTest(TestCase):
    def test_command_add_one_experiment(self):
        out = StringIO()
        call_command('add_experiment', '--public_number=CODE000', '--title=title first experiment',
                     '--description=description of the experiment',
                     '--beamline_code="COPRS"', stdout=out)
        self.assertIn("Successfully added experiment ", out.getvalue())

    def test_command_add_existing_experiment(self):
        out = StringIO()
        call_command('add_experiment', '--public_number=CODE000', '--title=title first experiment',
                     '--description=description of the experiment',
                     '--beamline_code="COPRS"', stdout=out)

        self.assertIn("Successfully added experiment", out.getvalue())

        with self.assertRaises(Exception):
            call_command('add_experiment', '--public_number=CODE000', '--title=another title first experiment',
                         '--description=description of the experiment',
                         '--beamline_code=COPRS', stdout=out)

    def test_command_add_three_experiments(self):
        out = StringIO()
        call_command('add_experiment', '--public_number=2018CODE000', '--title=TITLE001', '--description=my desc',
                     '--beamline_code="COPRS"', stdout=out)

        self.assertIn("Successfully added experiment", out.getvalue())

        call_command('add_experiment', '--public_number=2017CODE000', '--title=TITLE002', '--description=my desc',
                     '--beamline_code="COPRS"', stdout=out)

        self.assertIn("Successfully added experiment", out.getvalue())

        call_command('add_experiment', '--public_number=2016CODE000', '--title=TITLE003', '--description=my desc',
                     '--beamline_code="COPRS"', stdout=out)

        self.assertIn("Successfully added experiment", out.getvalue())
