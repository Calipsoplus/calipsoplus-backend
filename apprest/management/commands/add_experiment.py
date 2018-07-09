import logging

from django.core.management.base import BaseCommand, CommandError

from apprest.models.experiment import CalipsoExperiment

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Add experiment'

    def add_arguments(self, parser):
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)
        parser.add_argument('--title', dest='title', default='', help='The title of the experiment', type=str)
        parser.add_argument('--description', dest='description', default='', help='The description of the experiment',
                            type=str)
        parser.add_argument('--beamline_code', dest='beamline-code', default='',
                            help='The beam line code of experiment', type=str)

    def handle(self, *args, **options):
        logger.debug('####### DJANGO add_experiment command to Calipso   START #######')

        public_number = options['public_number']
        title = options['title']
        description = options['description']
        beamline_code = options['beamline-code']

        if not public_number or not title or not description or not beamline_code:
            raise CommandError(
                'python manage.py add_experiment --public_number public_number'
                ' --title title --decription description --beamline_code beam line coe')

        try:
            calipso_experiment = CalipsoExperiment.objects.filter(serial_number=public_number)
            if len(calipso_experiment) > 0:
                raise CommandError(
                    'The public number: %s, aready exists' % public_number)
            else:
                calipso_experiment = CalipsoExperiment()
                calipso_experiment.subject = title
                calipso_experiment.serial_number = public_number
                calipso_experiment.body = description
                calipso_experiment.beam_line = beamline_code

                calipso_experiment.save()
                logger.debug(self.style.SUCCESS('Successfully added experiment "%s"' % public_number))
                self.stdout.write(self.style.SUCCESS('Successfully added experiment "%s"' % public_number))

        except Exception as e:
            logger.debug(
                self.style.SUCCESS('Can not be able to add experiment with this public number: %s' % public_number))
            raise CommandError(
                'Can not be able to add experiment with this public number: %s, error:%s' % (public_number, e))