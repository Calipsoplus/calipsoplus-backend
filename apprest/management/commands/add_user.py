from django.core.management.base import BaseCommand, CommandError
from apprest.services.experiment import CalipsoExperimentsServices


class Command(BaseCommand):
    help = 'Add user to experiment'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--userlogin', dest='userlogin', default='', help='The username of experiment', type=str)
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)

    def handle(self, *args, **options):
        username = options['userlogin']
        public_number = options['public_number']

        if not username or not public_number:
            raise CommandError(
                'python manage.py add_user --userlogin username --public_number public_number')

        try:
            self.experiments_services.add_user_to_experiment(username=username, experiment=public_number)
            self.stdout.write(
                self.style.SUCCESS('Successfully added experiment %s to user %s' % (public_number, username)))

        except Exception as e:
            raise CommandError(
                'Can not be able to add experiment:%s to user: %s, error:%s' % (public_number, username, e))