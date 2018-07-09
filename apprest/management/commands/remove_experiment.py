import logging

from django.core.management.base import BaseCommand, CommandError

from apprest.models.experiment import CalipsoExperiment

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Remove experiment'

    def add_arguments(self, parser):
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)

    def handle(self, *args, **options):
        logger.debug('####### DJANGO remove_experiment command to Calipso   START #######')
        public_number = options['public_number']

        if not public_number:
            raise CommandError(
                'python manage.py remove_experiment --public_number code')

        try:
            CalipsoExperiment.objects.get(serial_number=public_number).delete()
            logger.debug(self.style.SUCCESS('Successfully removed experiment "%s"' % public_number))
            self.stdout.write(self.style.SUCCESS('Successfully removed experiment "%s"' % public_number))

        except Exception as e:
            logger.debug(
                self.style.SUCCESS('Can not be able to remove experiment with this public number: %s' % public_number))
            raise CommandError(
                'Can not be able to remove experiment with this public number: %s, error:%s' % (public_number, e))
