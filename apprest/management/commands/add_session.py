from django.core.management.base import BaseCommand, CommandError

from apprest.models import CalipsoExperiment
from apprest.services.session import CalipsoSessionsServices


class Command(BaseCommand):
    help = 'Add session'
    session_services = CalipsoSessionsServices()

    def add_arguments(self, parser):
        parser.add_argument('--public_number', dest='public_number', default='',
                            help='The public number of the experiment', type=str)

        parser.add_argument('--session_number', dest='session_number', default='', help='Session number', type=str)
        parser.add_argument('--start_date', dest='start_date', default='', help='Start date of the session',
                            type=str)
        parser.add_argument('--end_date', dest='end_date', default='', help='End date of the session',
                            type=str)

        parser.add_argument('--subject', dest='subject', default='', help='The subject of the session',
                            type=str)
        parser.add_argument('--body', dest='body', default='', help='The description of the session',
                            type=str)

        parser.add_argument('--data_set_path', dest='data_set_path', default='',
                            help='The beam line code of experiment', type=str)

    def handle(self, *args, **options):

        public_number = options['public_number']
        session_number = options['session_number']
        start_date = options['start_date']
        end_date = options['end_date']
        subject = options['subject']
        body = options['body']
        data_set_path = options['data_set_path']

        if not public_number or not session_number or not start_date or not end_date or not subject or not body or not data_set_path:
            raise CommandError(
                'python manage.py add_session --public_number public_number'
                ' --session_number session_number --start_date start_date --end_date end_date  --subject subject --body body --data_set_path data_set_path')

        try:
            experiment = CalipsoExperiment.objects.get(serial_number=public_number)

            params = {'session_number': session_number,
                      'start_date': start_date,
                      'end_date': end_date,
                      'subject': subject,
                      'body': body,
                      'data_set_path': data_set_path}


            self.session_services.create_session_to_experiment(params=params, experiment=experiment)

            self.stdout.write(self.style.SUCCESS('Successfully added session to experiment "%s"' % public_number))

        except Exception as e:
            raise CommandError(
                'Can not be able to add session with this public number: %s, error:%s' % (public_number, e))
