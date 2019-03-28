from django.core.management.base import BaseCommand, CommandError

from apprest.services.experiment import CalipsoExperimentsServices


class Command(BaseCommand):
    help = 'Update experiment from given data'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)
        parser.add_argument('--set_title', dest='title', default='', help='The title of the experiment', type=str)
        parser.add_argument('--set_description', dest='description', default='',
                            help='The description of the experiment',
                            type=str)
        parser.add_argument('--set_beamline_code', dest='beamline_code', default='',
                            help='The beam line code of experiment', type=str)
        parser.add_argument('--uid', dest='uid', default='',
                            help='The uid from experiment', type=str)
        parser.add_argument('--gid', dest='gid', default='',
                            help='The gid from experiment', type=str)

    def handle(self, *args, **options):
        public_number = options['public_number']
        title = options['title']
        description = options['description']
        beamline_code = options['beamline_code']
        uid = options['uid']
        gid = options['gid']

        if not public_number:
            raise CommandError(
                'python manage.py update_experiment --public_number public_number'
                ' --set_title title --set_decription description --set_beamline_code beam line code'
                ' --uid uid --gid gid')

        try:
            self.experiments_services.update_experiment(beamline_code, description, public_number, title, uid, gid)
            self.stdout.write(self.style.SUCCESS('Successfully updated experiment "%s"' % public_number))

        except Exception as e:
            raise CommandError(
                'Can not be able to updated experiment with this public number: %s, error:%s' % (public_number, e))