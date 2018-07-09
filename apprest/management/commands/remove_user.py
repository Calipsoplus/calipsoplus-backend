import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from apprest.models.experiment import CalipsoExperiment
from apprest.models.user import CalipsoUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Remove user from experiment'

    def add_arguments(self, parser):
        parser.add_argument('--userlogin', dest='userlogin', default='', help='The title of the experiment', type=str)
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)

    def handle(self, *args, **options):
        logger.debug('####### DJANGO remove_user command to Calipso   START #######')

        username = options['userlogin']
        public_number = options['public_number']

        if not public_number or not username:
            raise CommandError(
                'python manage.py remove_user --userlogin username --public_number public_number')

        try:
            user = User.objects.get(username=username)
            calipso_user = CalipsoUser.objects.get(user=user)
            calipso_experiment = CalipsoExperiment.objects.get(serial_number=public_number)

            calipso_user.experiments.remove(calipso_experiment)
            calipso_user.save()

            logger.debug(
                self.style.SUCCESS('Successfully removed user %s from experiment:%s' % (username, public_number)))
            self.stdout.write(
                self.style.SUCCESS('Successfully removed user %s from experiment:%s' % (username, public_number)))

        except Exception as e:
            logger.debug(
                self.style.SUCCESS(
                    'Can not be able to remove user:%s from experiment: %s, error:%s' % (username, public_number, e)))
            raise CommandError(
                'Can not be able to remove user:%s from experiment: %s, error:%s' % (username, public_number, e))