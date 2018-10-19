from django.core.management.base import BaseCommand, CommandError
from apprest.services.experiment import CalipsoExperimentsServices


class Command(BaseCommand):
    help = 'Remove experiment'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)

    def handle(self, *args, **options):
        public_number = options['public_number']

        if not public_number:
            raise CommandError(
                'python manage.py remove_experiment --public_number code')

        try:
            self.experiments_services.remove_experiment(public_number)
            self.stdout.write(self.style.SUCCESS('Successfully removed experiment "%s"' % public_number))

        except Exception as e:
            raise CommandError(
                'Can not be able to remove experiment with this public number: %s, error:%s' % (public_number, e))
