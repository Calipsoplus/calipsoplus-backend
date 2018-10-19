import logging
from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class AddUserCommandTest(TestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['users.json', 'experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

    def test_command_add_one_user_that_not_exists(self):
        out = StringIO()

        with self.assertRaises(Exception):
            call_command('add_user', '--userlogin=acampsm', '--public_number=CODE000', stdout=out)

    def test_command_add_experiment_to_one_user_that_exists(self):
        out = StringIO()

        call_command('add_user', '--userlogin=userA', '--public_number=2018091632', stdout=out)
        self.assertIn("Successfully added experiment", out.getvalue())

