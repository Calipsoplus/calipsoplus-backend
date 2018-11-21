from django.core.management.base import BaseCommand, CommandError



import csv

from apprest.models import CalipsoExperiment
from apprest.services.session import CalipsoSessionsServices


class Command(BaseCommand):
    help = 'Add sessions from csv file'
    sessions_services = CalipsoSessionsServices()

    def add_arguments(self, parser):
        parser.add_argument('--path', dest='path', default='', help='absolute csv filename path', type=str)

    def handle(self, *args, **options):
        done = 0
        path = options['path']

        if not path:
            raise CommandError(
                'python manage.py add_session_csv --path absolute-file-path')
        try:
            with open(path) as csv_file:
                reader = csv.DictReader(csv_file)
                for line, row in enumerate(reader, start=2):
                    public_number = row['public_number']
                    session_number = row['session_number']
                    start_date = row['start_date']
                    end_date = row['end_date']
                    subject = row['subject']
                    body = row['body']
                    data_set_path = row['data_set_path']

                    try:

                        experiment = CalipsoExperiment.objects.get(serial_number=public_number)

                        params = {'session_number': session_number,
                                  'start_date': start_date,
                                  'end_date': end_date,
                                  'subject': subject,
                                  'body': body,
                                  'data_set_path': data_set_path}


                        self.sessions_services.create_session_to_experiment(params=params,
                                                                           experiment=experiment)


                        self.stdout.write(self.style.SUCCESS('line %d ..%s Ok!' % (line, session_number)))
                        done += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR('line %d error:%s' % (line, e)))

            self.stdout.write(self.style.SUCCESS('File processed. %d/%d done.!' % (done, line-1)))

        except Exception as e:
            raise CommandError('Problems, %s' % e)