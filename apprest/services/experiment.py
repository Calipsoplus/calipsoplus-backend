import datetime
import json
import logging

import requests
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.exceptions import NotFound

from apprest.models import CalipsoSession
from apprest.models.experiment import CalipsoExperiment, CalipsoUserExperiment
from apprest.models.user import CalipsoUser

from calipsoplus.settings_calipso import PAGE_SIZE_EXPERIMENTS


def get_str(content):
    if not content:
        return '.'
    return str(content)


class CalipsoExperimentsServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_user_experiments(self, username):
        self.logger.debug('Getting get_user_experiments from user_id %s' % username)
        try:
            user = User.objects.get(username=username)
            calipso_user = CalipsoUser.objects.get(user=user)
            experiments = CalipsoExperiment.objects.filter(calipso_users=calipso_user).all()
            return experiments
        except User.DoesNotExist as dne:
            self.logger.debug(dne)
            raise NotFound(detail='User not found')
        except Exception as e:
            self.logger.debug(e)
            raise e

    def add_user_to_experiment(self, username, public_number):
        self.logger.debug('Adding user: %s to experiment: %s' % (username, public_number))
        user = User.objects.get(username=username)
        calipso_user = CalipsoUser.objects.get(user=user)
        experiment = CalipsoExperiment.objects.get(proposal_id=public_number)

        calipso_user_experiment = CalipsoUserExperiment.objects.filter(calipso_user=calipso_user,
                                                                       calipso_experiment=experiment)

        if len(calipso_user_experiment) > 0:
            raise Exception('User %s already has experiment %s.' % (username, public_number))
        else:
            calipso_user_experiment = CalipsoUserExperiment(calipso_user=calipso_user, calipso_experiment=experiment)
            calipso_user_experiment.save()

    def add_experiment(self, public_number, title, description, beamline_code):
        self.logger.debug('Try to add experiment %s' % public_number)
        calipso_experiment = CalipsoExperiment.objects.filter(proposal_id=public_number)
        if len(calipso_experiment) > 0:
            raise Exception('Experiment %s already exists.' % public_number)
        else:
            calipso_experiment = CalipsoExperiment()
            calipso_experiment.subject = title
            calipso_experiment.proposal_id = public_number
            calipso_experiment.body = description
            calipso_experiment.beam_line = beamline_code

            calipso_experiment.save()

    def remove_experiment(self, public_number):
        self.logger.debug('Try to remove experiment %s' % public_number)
        CalipsoExperiment.objects.get(proposal_id=public_number).delete()

    def remove_user_from_experiment(self, username, public_number):
        self.logger.debug('Try to remove user %s from experiment %s' % (username, public_number))
        user = User.objects.get(username=username)
        calipso_user = CalipsoUser.objects.get(user=user)
        calipso_experiment = CalipsoExperiment.objects.get(proposal_id=public_number)

        calipso_user_experiment = CalipsoUserExperiment.objects.get(calipso_user=calipso_user,
                                                                    calipso_experiment=calipso_experiment)

        calipso_user_experiment.delete()

    def update_experiment(self, beamline_code, description, public_number, title):
        self.logger.debug('Try to update experiment %s' % public_number)
        calipso_experiment = CalipsoExperiment.objects.get(proposal_id=public_number)

        if title:
            calipso_experiment.subject = title
        if description:
            calipso_experiment.body = description
        if beamline_code:
            calipso_experiment.beam_line = beamline_code

        calipso_experiment.save()

    def get_external_user_experiments(self, username, query):
        self.logger.debug('Getting get_external_user_experiments from user:%s' % username)
        try:
            url = settings.DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL_ENDPOINT.replace('$USERNAME', username)
            self.logger.debug('calling external endpoint %s' % url)

            response = requests.get(url, params=query, auth=(
                settings.LOCAL_ACCESS_USERNAME, settings.LOCAL_ACCESS_PASSWORD))

            response.json()['page_size'] = PAGE_SIZE_EXPERIMENTS

            return response.json()

        except Exception as e:
            self.logger.debug(e)
            raise e

    def get_external_is_authorized(self, username):

        self.logger.debug('calling external endpoint to obtain if is authorized (%s)' % username)
        try:
            url = settings.BACKEND_UO_IS_AUTHORIZED

            post_data = {'login': username}
            headers = {'Content-type': 'application/json'}

            response = requests.post(url, data=json.dumps(post_data), headers=headers, auth=(
                settings.LOCAL_ACCESS_USERNAME, settings.LOCAL_ACCESS_PASSWORD))

            if response.status_code != 200:
                return {'result': False}
            else:
                return response.json()

        except Exception as e:
            self.logger.debug(e)
            return {'result': False}

    def update_favorite_from_external_experiments(self, username, experiments_list):
        self.logger.debug('filling external experiments with favorite values')

        for experiment in experiments_list['results']:
            result = self.persist_proposals_favorites(username, experiment)
            experiment['favorite'] = result[0]
            experiment['id'] = result[1]

        return experiments_list

    def persist_proposals_favorites(self, username, experiments):
        try:
            subject = experiments.get('subject')
            body = experiments.get('body')
            proposal_id = experiments.get('proposal_id')
            beam_line = experiments.get('beam_line')

            subject = get_str(content=subject)
            body = get_str(content=body)
            beam_line = get_str(content=beam_line)

            # experiments
            try:
                exp = CalipsoExperiment.objects.get(proposal_id=proposal_id)
                exp.subject = subject
                exp.body = body
                exp.beam_line = beam_line
                exp.save()
            except CalipsoExperiment.DoesNotExist as e:
                self.logger.debug("UserExperiment not found: %s" % e)
                exp = CalipsoExperiment.objects.create(subject=subject, body=body,
                                                       proposal_id=proposal_id,
                                                       beam_line=beam_line)
            # sessions
            for session in experiments.get('sessions'):

                session_number = session.get('session_number')
                session_start_date = datetime.datetime.strptime(session.get('start_date'), "%Y-%m-%dT%H:%M:%SZ")
                session_end_date = datetime.datetime.strptime(session.get('start_date'), "%Y-%m-%dT%H:%M:%SZ")
                session_subject = session.get('subject')
                session_body = session.get('body')
                session_data_set_path = session.get('date_set_path')

                if not session_data_set_path:
                    session_data_set_path = "[]"

                self.logger.debug("Session loop %s" % session_number)
                session_subject = get_str(content=session_subject)
                session_body = get_str(content=session_body)

                try:
                    sess = CalipsoSession.objects.get(session_number=session_number, experiment=exp)
                    sess.session_number = sess.session_number
                    sess.start_date = session_start_date
                    sess.end_date = session_end_date
                    sess.body = session_body
                    sess.subject = session_subject
                    sess.save()

                except Exception as e:

                    self.logger.debug("Session not found: %s" % e)
                    sess = CalipsoSession(session_number=session_number, start_date=session_start_date,
                                          end_date=session_end_date, subject=session_subject,
                                          body=session_body, data_set_path=session_data_set_path,
                                          experiment=exp)
                    sess.save()

            try:
                user = User.objects.get(username=username)
                calipso_user = CalipsoUser.objects.get(user=user)

                try:
                    self.logger.debug("Try to get user_experiment %s,%s" % (username, exp.id))
                    user_experiment = CalipsoUserExperiment.objects.get(calipso_user=calipso_user,
                                                                        calipso_experiment=exp)
                except Exception as e:
                    self.logger.debug("Creating new user(%s)_experiment(%s) e:%s" % (username, exp.id, e))
                    user_experiment = CalipsoUserExperiment(calipso_user=calipso_user, calipso_experiment=exp,
                                                            favorite=False)
                    user_experiment.save()
                return user_experiment.favorite, user_experiment.id

            except Exception as e:
                self.logger.debug("UserExperiment not found: %s" % e)
                return False, 0

        except Exception as e:
            self.logger.debug("Error CalipsoExperiment creation: %s" % e)
            return False, 0
