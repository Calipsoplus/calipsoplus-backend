import logging
from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class RemoveUserCommandTest(TestCase):
    logger = logging.getLogger(__name__)

    fixtures = ['users.json', 'experiments.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

    def test_command_remove_existent_user_experiment(self):
        out = StringIO()

        call_command('remove_user', '--userlogin=userA', '--public_number=2018091632', stdout=out)

        self.assertIn("Successfully removed user", out.getvalue())

    def test_command_remove_nonexistent_user_from_experiment(self):
        out = StringIO()

        with self.assertRaises(Exception):
            call_command('remove_user', '--userlogin=acampsm', '--public_number=2018091632', stdout=out)

    def test_command_remove_existent_user_experiment(self):
        out = StringIO()

        call_command('remove_user', '--userlogin=userA', '--public_number=2018091632', stdout=out)

        self.assertIn("Successfully removed user", out.getvalue())

    def test_command_remove_existent_user_from_non_existent_experiment(self):
        out = StringIO()

        with self.assertRaises(Exception):
            call_command('remove_user', '--userlogin=usrA', '--public_number=AAAR91632', stdout=out)