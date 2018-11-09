from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from apprest.services.experiment import CalipsoExperimentsServices

import csv


class Command(BaseCommand):
    help = 'Inserts users from csv file'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--path', dest='path', default='', help='Absolute csv filename path', type=str)

    def handle(self, *args, **options):
        done = 0
        path = options['path']

        if not path:
            raise CommandError(
                'python manage.py insert_users_csv --path=absolute-file-path')
        try:
            with open(path) as csv_file:
                reader = csv.DictReader(csv_file)
                for line, row in enumerate(reader, start=2):
                    username = row['userlogin']

                    try:
                        User.objects.get(username=username)
                        self.stdout.write(self.style.ERROR('line %d, User %s already exists' % (line,username)))

                    except User.DoesNotExist as udne:
                        new_user = User.objects.create_user(username, '')
                        new_user.save()
                        self.stdout.write(
                            self.style.SUCCESS('line %d Successfully inserted user %s' % (line, username)))
                        done += 1


            self.stdout.write(self.style.SUCCESS('File processed. %d/%d done.!' % (done, line-1)))

        except Exception as e:
            raise CommandError('Problems, %s' % e)