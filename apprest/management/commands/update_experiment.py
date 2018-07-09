import logging

from django.core.management.base import BaseCommand, CommandError

from apprest.models.experiment import CalipsoExperiment

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update experiment from given data'

    def add_arguments(self, parser):
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)
        parser.add_argument('--set_title', dest='title', default='', help='The title of the experiment', type=str)
        parser.add_argument('--set_description', dest='description', default='', help='The description of the experiment',
                            type=str)
        parser.add_argument('--set_beamline-code', dest='beamline_code', default='',
                            help='The beam line code of experiment', type=str)

    def handle(self, *args, **options):
        logger.debug('####### DJANGO update_experiment command to Calipso   START #######')

        public_number = options['public_number']
        title = options['title']
        description = options['description']
        beamline_code = options['beamline_code']

        if not public_number:
            raise CommandError(
                'python manage.py update_experiment --public_number public_number'
                ' --set_title title --set_decription description --set_beamline-code beam line coe')

        try:
            calipso_experiment = CalipsoExperiment.objects.get(serial_number=public_number)

            if title:
                calipso_experiment.subject = title
            if description:
                calipso_experiment.body = description

            if beamline_code:
                calipso_experiment.beam_line = beamline_code

            calipso_experiment.save()
            logger.debug(self.style.SUCCESS('Successfully updated experiment "%s"' % public_number))
            self.stdout.write(self.style.SUCCESS('Successfully updated experiment "%s"' % public_number))

        except Exception as e:
            logger.debug(
                self.style.SUCCESS('Can not be able to updated experiment with this public number: %s' % public_number))
            raise CommandError(
                'Can not be able to updated experiment with this public number: %s, error:%s' % (public_number, e))


