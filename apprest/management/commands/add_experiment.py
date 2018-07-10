from django.core.management.base import BaseCommand, CommandError

from apprest.services.experiment import CalipsoExperimentsServices


class Command(BaseCommand):
    help = 'Add experiment'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)
        parser.add_argument('--title', dest='title', default='', help='The title of the experiment', type=str)
        parser.add_argument('--description', dest='description', default='', help='The description of the experiment',
                            type=str)
        parser.add_argument('--beamline_code', dest='beamline_code', default='',
                            help='The beam line code of experiment', type=str)

    def handle(self, *args, **options):

        public_number = options['public_number']
        title = options['title']
        description = options['description']
        beamline_code = options['beamline_code']

        if not public_number or not title or not description or not beamline_code:
            raise CommandError(
                'python manage.py add_experiment --public_number public_number'
                ' --title title --description description --beamline_code beam line coe')

        try:
            self.experiments_services.add_experiment(beamline_code, description, public_number, title)
            self.stdout.write(self.style.SUCCESS('Successfully added experiment "%s"' % public_number))

        except Exception as e:
            raise CommandError(
                'Can not be able to add experiment with this public number: %s, error:%s' % (public_number, e))

