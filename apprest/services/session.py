import logging

from apprest.models.session import CalipsoSession


class CalipsoSessionsServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_sessions_from_experiment(self, experiment):
        self.logger.debug('get_sessions_from_experiment from experiment %s' % experiment.serial_number)
        try:
            sessions = CalipsoSession.objects.filter(experiment_id=experiment.id).all()
            return sessions

        except Exception as e:
            self.logger.debug(e)
            raise e

    def create_session_to_experiment(self, session_number, start_date, end_date, subject, body,
                                     data_set_path, experiment):
        self.logger.debug('create_session_to_experiment from experiment %s' % experiment.serial_number)

        calipso_session = CalipsoSession.objects.filter(session_number=session_number)
        if len(calipso_session) > 0:
            raise Exception('Session %s already exists.' % session_number)
        else:
            try:

                session = CalipsoSession(session_number=session_number, start_date=start_date, end_date=end_date,
                                         subject=subject, body=body, data_set_path=data_set_path, experiment=experiment)
                session.save()

            except Exception as e:
                self.logger.debug(e)
                raise e
