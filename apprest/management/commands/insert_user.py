from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from apprest.services.experiment import CalipsoExperimentsServices


class Command(BaseCommand):
    help = 'Insert new user'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--userlogin', dest='userlogin', default='', help='The username', type=str)

    def handle(self, *args, **options):
        username = options['userlogin']

        if not username:
            raise CommandError(
                'python manage.py insert_user --userlogin username')

        try:
            User.objects.get(username=username)
            self.stdout.write(self.style.ERROR('User %s already exists' % username))

        except User.DoesNotExist as udne:
            new_user = User.objects.create_user(username, '')
            new_user.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted user %s' % username))
