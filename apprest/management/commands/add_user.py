import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from apprest.models.experiment import CalipsoExperiment
from apprest.models.user import CalipsoUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Add user to experiment'

    def add_arguments(self, parser):
        parser.add_argument('--userlogin', dest='userlogin', default='', help='The username of experiment', type=str)
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)

    def handle(self, *args, **options):
        logger.debug('####### DJANGO add_user command to Calipso   START #######')

        username = options['userlogin']
        public_number = options['public_number']

        if not username or not public_number:
            raise CommandError(
                'python manage.py add_user --userlogin username --public_number public_number')

        try:
            user = User.objects.get(username=username)
            calipso_user = CalipsoUser.objects.get(user=user)
            calipso_experiment = CalipsoExperiment.objects.get(serial_number=public_number)
            calipso_user.experiments.add(calipso_experiment)
            calipso_user.save()
            logger.debug(self.style.SUCCESS('Successfully added experiment %s to user %s' % (public_number, username)))
            self.stdout.write(
                self.style.SUCCESS('Successfully added experiment %s to user %s' % (public_number, username)))

        except Exception as e:
            logger.debug(
                self.style.SUCCESS(
                    'Can not be able to add experiment:%s to  user:%s, error:%s' % (public_number, username, e)))
            raise CommandError(
                'Can not be able to add experiment:%s to user: %s, error:%s' % (public_number, username, e))