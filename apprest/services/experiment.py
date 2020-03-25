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

from calipsoplus.settings_calipso import PAGE_SIZE_EXPERIMENTS, BACKEND_DEFAULT_AUTHORIZATION

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def get_str(content):
    if not content:
        return '.'
    return str(content)

def json_default(value):
    if isinstance(value, datetime.date):
        return datetime.datetime(value.year,value.month,value.day, value.hour, value.minute, value.second).strftime(DATE_TIME_FORMAT)
    else:
        return value.__dict__


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

    def add_experiment(self, public_number, title, description, beamline_code, uid, gid):
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
            calipso_experiment.uid = uid
            calipso_experiment.gid = gid

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

    def update_experiment(self, beamline_code, description, public_number, title, uid, gid):
        self.logger.debug('Try to update experiment %s' % public_number)
        calipso_experiment = CalipsoExperiment.objects.get(proposal_id=public_number)

        if title:
            calipso_experiment.subject = title
        if description:
            calipso_experiment.body = description
        if beamline_code:
            calipso_experiment.beam_line = beamline_code
        if uid:
            calipso_experiment.uid = uid
        if gid:
            calipso_experiment.gid = gid

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




    def get_icat_experiments_sort_search(self, username, query, experiments_list):
        search_field = query['search']
        ordering_field = query['ordering']

        object_list = []

        if search_field is not None:
            for obj in experiments_list:
                append = False
                try:
                    obj.beam_line.index(search_field)
                    append = True
                except Exception:
                    pass
                try:
                    obj.subject.index(search_field)
                    append = True
                except Exception:
                    pass
                try:
                    obj.body.index(search_field)
                    append = True
                except Exception:
                    pass
                try:
                    obj.proposal_id.index(search_field)
                    append = True
                except Exception:
                    pass
                if append:
                    object_list.append(obj)

            experiments_list = object_list

        if ordering_field != '':
            try:
                object_list = experiments_list
                if ordering_field == "proposal_id":
                    my_sorted_data = sorted(object_list, key=lambda k: k.proposal_id, reverse=True)
                elif ordering_field == "-proposal_id":
                    my_sorted_data = sorted(object_list, key=lambda k: k.proposal_id, reverse=False)
                if ordering_field == "subject":
                    my_sorted_data = sorted(object_list, key=lambda k: k.subject, reverse=True)
                elif ordering_field == "-subject":
                    my_sorted_data = sorted(object_list, key=lambda k: k.subject, reverse=False)
                if ordering_field == "beam_line":
                    my_sorted_data = sorted(object_list, key=lambda k: k.beam_line, reverse=True)
                elif ordering_field == "-beam_line":
                    my_sorted_data = sorted(object_list, key=lambda k: k.beam_line, reverse=False)
                if ordering_field == "body":
                    my_sorted_data = sorted(object_list, key=lambda k: k.body, reverse=True)
                elif ordering_field == "-body":
                    my_sorted_data = sorted(object_list, key=lambda k: k.body, reverse=False)
                experiments_list = my_sorted_data
            except Exception:
                object_list = []

        return json.loads(json.dumps(experiments_list, default=json_default))

    def get_external_is_authorized(self, username):

        self.logger.debug('Check authorization for (%s)' % username)
        if BACKEND_DEFAULT_AUTHORIZATION == 1:
            return {'result': True}

        self.logger.debug('Calling external endpoint to check if is authorized (%s)' % username)
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
            uid = experiments.get('uid')
            gid = experiments.get('gid')

            subject = get_str(content=subject)
            body = get_str(content=body)
            beam_line = get_str(content=beam_line)
            uid = get_str(content=uid)
            gid = get_str(content=gid)

            # experiments
            try:
                exp = CalipsoExperiment.objects.get(proposal_id=proposal_id)
                exp.subject = subject
                exp.body = body
                exp.beam_line = beam_line
                exp.uid = uid
                exp.gid = gid
                exp.save()
            except CalipsoExperiment.DoesNotExist as e:
                self.logger.debug("UserExperiment not found: %s" % e)
                exp = CalipsoExperiment.objects.create(subject=subject, body=body,
                                                       proposal_id=proposal_id,
                                                       beam_line=beam_line,
                                                       uid=uid,
                                                       gid=gid)
            # sessions
            for session in experiments.get('sessions'):

                session_number = session.get('session_number')

                start_datetime = session.get('start_date')
                end_datetime = session.get('end_date')

                try:
                    session_start_date = datetime.datetime.strptime(start_datetime, DATE_TIME_FORMAT)
                    session_end_date = datetime.datetime.strptime(end_datetime, DATE_TIME_FORMAT)
                except Exception as e:
                    session_start_date = datetime.datetime(start_datetime['year'], start_datetime['month'], start_datetime['day']).strftime(DATE_TIME_FORMAT)
                    session_end_date = datetime.datetime(end_datetime['year'], end_datetime['month'], end_datetime['day']).strftime(DATE_TIME_FORMAT)

                session_subject = session.get('subject')
                session_body = session.get('body')
                session_data_set_path = session.get('data_set_path')

                if not session_data_set_path:
                    session_data_set_path = "[]"

                self.logger.debug("Session loop %s" % session_number)
                session_subject = get_str(content=session_subject)
                session_body = get_str(content=session_body)

                try:
                    sess = CalipsoSession.objects.get(session_number=session_number, experiment=exp)
                    sess.start_date = session_start_date
                    sess.end_date = session_end_date
                    sess.body = session_body
                    sess.subject = session_subject
                    sess.data_set_path = session_data_set_path
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

    def get_experiment(self, proposal_id):
        self.logger.debug('Getting one experiment: %s' % proposal_id)
        try:
            experiment = CalipsoExperiment.objects.get(proposal_id=proposal_id)
            self.logger.debug('Experiment found')
            return experiment

        except Exception as e:
            self.logger.warning("proposal_id = %s, not found." % proposal_id)
            self.logger.warning(e)
            raise Exception
