from django.core.management.base import BaseCommand, CommandError

from apprest.services.experiment import CalipsoExperimentsServices

import csv


class Command(BaseCommand):
    help = 'Add users from csv file'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--path', dest='path', default='', help='absolute csv filename path', type=str)

    def handle(self, *args, **options):
        done = 0
        path = options['path']

        if not path:
            raise CommandError(
                'python manage.py add_user_csv --path absolute-file-path')
        try:
            with open(path) as csv_file:
                reader = csv.DictReader(csv_file)
                for line, row in enumerate(reader, start=2):
                    public_number = row['public_number']
                    userlogin = row['userlogin']

                    try:
                        self.experiments_services.add_user_to_experiment(userlogin, public_number)
                        self.stdout.write(self.style.SUCCESS('line %d .%s. %s Ok!' % (line, userlogin, public_number)))
                        done += 1
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR('line %d .%s. %s Error! e:%s' % (line, userlogin, public_number, e)))


            self.stdout.write(self.style.SUCCESS('File processed. %d/%d done.!' % (done, line-1)))

        except Exception as e:
            raise CommandError('Problems, %s' % e)