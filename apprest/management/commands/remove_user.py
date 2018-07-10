from django.core.management.base import BaseCommand, CommandError
from apprest.services.experiment import CalipsoExperimentsServices


class Command(BaseCommand):
    help = 'Remove user from experiment'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--userlogin', dest='userlogin', default='', help='The title of the experiment', type=str)
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)

    def handle(self, *args, **options):
        username = options['userlogin']
        public_number = options['public_number']

        if not public_number or not username:
            raise CommandError(
                'python manage.py remove_user --userlogin username --public_number public_number')

        try:
            self.experiments_services.remove_user_from_experiment(username, public_number)

            self.stdout.write(
                self.style.SUCCESS('Successfully removed user %s from experiment:%s' % (username, public_number)))

        except Exception as e:
            raise CommandError(
                'Can not be able to remove user:%s from experiment: %s, error:%s' % (username, public_number, e))