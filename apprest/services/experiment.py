import logging

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework.exceptions import NotFound

from apprest.models.experiment import CalipsoExperiment, CalipsoUserExperiment
from apprest.models.user import CalipsoUser


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
        experiment = CalipsoExperiment.objects.get(serial_number=public_number)

        calipso_user_experiment = CalipsoUserExperiment.objects.filter(calipso_user=calipso_user,
                                                                       calipso_experiment=experiment)

        if len(calipso_user_experiment) > 0:
            raise Exception('User %s already has experiment %s.' % (username, public_number))
        else:
            calipso_user_experiment = CalipsoUserExperiment(calipso_user=calipso_user, calipso_experiment=experiment)
            calipso_user_experiment.save()

    def add_experiment(self, public_number, title, description, beamline_code):
        self.logger.debug('Try to add experiment %s' % public_number)
        calipso_experiment = CalipsoExperiment.objects.filter(serial_number=public_number)
        if len(calipso_experiment) > 0:
            raise Exception('Experiment %s already exists.' % public_number)
        else:
            calipso_experiment = CalipsoExperiment()
            calipso_experiment.subject = title
            calipso_experiment.serial_number = public_number
            calipso_experiment.body = description
            calipso_experiment.beam_line = beamline_code

            calipso_experiment.save()

    def remove_experiment(self, public_number):
        self.logger.debug('Try to remove experiment %s' % public_number)
        CalipsoExperiment.objects.get(serial_number=public_number).delete()

    def remove_user_from_experiment(self, username, public_number):
        self.logger.debug('Try to remove user %s from experiment %s' % (username, public_number))
        user = User.objects.get(username=username)
        calipso_user = CalipsoUser.objects.get(user=user)
        calipso_experiment = CalipsoExperiment.objects.get(serial_number=public_number)

        calipso_user_experiment = CalipsoUserExperiment.objects.get(calipso_user=calipso_user,
                                                                    calipso_experiment=calipso_experiment)

        calipso_user_experiment.delete()

    def update_experiment(self, beamline_code, description, public_number, title):
        self.logger.debug('Try to update experiment %s' % public_number)
        calipso_experiment = CalipsoExperiment.objects.get(serial_number=public_number)

        if title:
            calipso_experiment.subject = title
        if description:
            calipso_experiment.body = description
        if beamline_code:
            calipso_experiment.beam_line = beamline_code

        calipso_experiment.save()

    def get_external_user_experiments(self, username, query):
        self.logger.debug('Getting get_external_user_experiments from user:%s' % username)
        """
         query = {page, ordering, search, calipsouserexperiment__favorite}
        """

        try:
            url = settings.DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL_ENDPOINT.replace('$USERNAME', username)

            self.logger.debug('calling external endpoint %s' % url)
            # response = requests.get(url, params=query, verify=False)

            headers = {'Content-type': 'application/json'}
            response = requests.get(url, params=query, headers=headers)

            """
                next
                previous
                cont
                results
                    serial_number
                    subject
                    body
                    beam_line
                    sessions
                        session_number
                        start_date
                        end_date
                        subject
                        body
                        data_set_path
                    id
                    favorite
                page_size
            """

            experiments_list = {
                "next": None,
                "previous": None,
                "count": 2,
                "results": [
                    {
                        "serial_number": "A0001",
                        "subject": "Title un",
                        "body": "Description 1",
                        "beam_line": "BL_A",
                        "sessions": [
                            {
                                "session_number": "S0011",
                                "start_date": "2018-10-10T10:30:00",
                                "end_date": "2018-10-11T18:00:00",
                                "subject": "SUBJECT S11",
                                "body": "BODY S11",
                                "data_set_path": "{'/tmp/results/': {'bind': '', 'mode': 'rw'},'/tmp/data/': {'bind': '', 'mode': 'ro'}}"
                            },
                            {
                                "session_number": "S0012",
                                "start_date": "2018-10-10T11:00:00",
                                "end_date": "2018-10-12T18:00:00",
                                "subject": "SUBJECT S12",
                                "body": "BODY S12",
                                "data_set_path": "{'/tmp/results/': {'bind': '', 'mode': 'rw'},'/tmp/data/': {'bind': '', 'mode': 'ro'}}"
                            },
                            {
                                "session_number": "S0013",
                                "start_date": "2018-10-11T12:30:00",
                                "end_date": "2018-10-13T18:00:00",
                                "subject": "SUBJECT S13",
                                "body": "BODY S13",
                                "data_set_path": "{'/tmp/results/': {'bind': '', 'mode': 'rw'},'/tmp/data/': {'bind': '', 'mode': 'ro'}}"
                            },
                            {
                                "session_number": "S0014",
                                "start_date": "2018-10-12T13:00:00",
                                "end_date": "2018-10-14T18:00:00",
                                "subject": "SUBJECT S14",
                                "body": "BODY S14",
                                "data_set_path": "{'/tmp/results/': {'bind': '', 'mode': 'rw'},'/tmp/data/': {'bind': '', 'mode': 'ro'}}"
                            }
                        ],
                        "id": 1,
                        "favorite": False
                    },
                    {
                        "serial_number": "A0002",
                        "subject": "Title dos",
                        "body": "Description 2",
                        "beam_line": "BL_A",
                        "sessions": [
                            {
                                "session_number": "S0021",
                                "start_date": "2018-10-13T08:00:00",
                                "end_date": "2018-10-15T18:00:00",
                                "subject": "SUBJECT S21",
                                "body": "BODY S21",
                                "data_set_path": "{'/tmp/results/': {'bind': '', 'mode': 'rw'},'/tmp/data/': {'bind': '', 'mode': 'ro'}}"
                            },
                            {
                                "session_number": "S0022",
                                "start_date": "2018-10-14T09:30:00",
                                "end_date": "2018-10-16T18:00:00",
                                "subject": "SUBJECT S22",
                                "body": "BODY S22",
                                "data_set_path": "{'/tmp/results/': {'bind': '', 'mode': 'rw'},'/tmp/data/': {'bind': '', 'mode': 'ro'}}"
                            }
                        ],
                        "id": 2,
                        "favorite": True
                    }
                ],
                "page_size": 7
            }

            return response.json()



        except Exception as e:
            self.logger.debug(e)
            raise e


"""
            client = requests.session()
            client.get(URL)

            cookies = dict(client.cookies)
            r = requests.post(URL + "au", data=json.dumps(data), headers=headers, cookies=cookies)

            response = requests.get(url, params=query)

"""
