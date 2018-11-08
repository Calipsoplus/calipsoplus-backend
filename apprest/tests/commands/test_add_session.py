import logging
from io import StringIO
from django.core.management import call_command
from django.test import TestCase

logger = logging.getLogger(__name__)


class AddSessionToExperimentCommandTest(TestCase):

    fixtures = ['experiments.json']


    def setUp(self):
        logger.info('AddSessionToExperimentCommandTest')

    def test_command_add_one_session_to_existing_experiment(self):
        out = StringIO()
        call_command('add_session', '--public_number=2018091622', '--session_number=SS01',
                     '--start_date=2017-06-08T00:00:00',
                     '--end_date=2017-06-08T00:00:00',
                     '--subject=description session1',
                     '--body=body session1',
                     '--data_set_path=/var/user/joe', stdout=out)

        self.assertIn("Successfully added session ", out.getvalue())


    def test_command_add_one_session_to_none_existing_experiment(self):
        out = StringIO()

        with self.assertRaises(Exception):
            call_command('add_session', '--public_number=XXXX', '--session_number=SS01',
                     '--start_date=2017-06-08T00:00:00',
                     '--end_date=2017-06-08T00:00:00',
                     '--subject=description session1',
                     '--body=body session1',
                     '--data_set_path=/var/user/joe', stdout=out)



"""
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
"""