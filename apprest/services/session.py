import json
import logging

from apprest.models.session import CalipsoSession
from calipsoplus.settings_calipso import EXPERIMENTS_OUTPUT, EXPERIMENTS_DATASETS_ROOT


class CalipsoSessionsServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_sessions_from_experiment(self, experiment):
        self.logger.debug('get_sessions_from_experiment from experiment %s' % experiment.proposal_id)
        try:
            sessions = CalipsoSession.objects.filter(experiment_id=experiment.id).all()
            return sessions

        except Exception as e:
            self.logger.debug(e)
            raise e

    def create_session_to_experiment(self, params, experiment):

        session_number = params["session_number"]
        start_date = params["start_date"]
        end_date = params["end_date"]
        subject = params["subject"]
        body = params["body"]
        data_set_path = params["data_set_path"]

        self.logger.debug('create_session_to_experiment from experiment %s' % experiment.proposal_id)

        calipso_session = CalipsoSession.objects.filter(session_number=session_number)
        if len(calipso_session) > 0:
            raise Exception('Session %s already exists.' % session_number)
        else:
            try:
                calipso_session_volume = data_set_path.replace("'", "\"")
                json.loads(calipso_session_volume)

            except Exception as e:
                raise Exception('Session %s has an invalid json data_path. %s ' % (session_number, data_set_path))

            try:

                session = CalipsoSession(session_number=session_number, start_date=start_date, end_date=end_date,
                                         subject=subject, body=body, data_set_path=data_set_path, experiment=experiment)
                session.save()

            except Exception as e:
                self.logger.debug(e)
                raise e

    def get_volumes_from_session(self, session_number):
        self.logger.debug("get_volumes_from_session %s" % session_number)

        try:
            session = CalipsoSession.objects.get(session_number=session_number)
            calipso_session_volume = session.data_set_path.replace("'", "\"")
            session_volumes = json.loads(calipso_session_volume)

            for key in session_volumes.keys():
                if session_volumes[key]['mode'] == 'ro':
                    session_volumes[key]['bind'] = EXPERIMENTS_DATASETS_ROOT + session_volumes[key]['bind']
                if session_volumes[key]['mode'] == 'rw':
                    session_volumes[key]['bind'] = EXPERIMENTS_OUTPUT + session_volumes[key]['bind']

            self.logger.debug("volumes: %s" % session_volumes)

            return session_volumes

        except Exception as e:
            raise e
