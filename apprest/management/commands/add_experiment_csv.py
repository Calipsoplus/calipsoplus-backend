from django.core.management.base import BaseCommand, CommandError

from apprest.services.experiment import CalipsoExperimentsServices

import csv


class Command(BaseCommand):
    help = 'Add experiment from csv file'
    experiments_services = CalipsoExperimentsServices()

    def add_arguments(self, parser):
        parser.add_argument('--path', dest='path', default='', help='absolute csv filename path', type=str)

    def handle(self, *args, **options):
        done = 0
        path = options['path']

        if not path:
            raise CommandError(
                'python manage.py add_experiment_csv --path absolute-file-path')
        try:
            with open(path) as csv_file:
                reader = csv.DictReader(csv_file)
                for line, row in enumerate(reader, start=2):
                    public_number = row['public_number']
                    title = row['title']
                    description = row['description']
                    beamline_code = row['beamline_code']
                    uid = row['uid']
                    gid = row['gid']

                    try:
                        self.experiments_services.add_experiment(public_number, title, description, beamline_code, uid,
                                                                 gid)
                        self.stdout.write(self.style.SUCCESS('line %d ..%s Ok!' % (line, public_number)))
                        done += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR('line %d error:%s' % (line, e)))

            self.stdout.write(self.style.SUCCESS('File processed. %d/%d done.!' % (done, line - 1)))

        except Exception as e:
            raise CommandError('Problems, %s' % e)
