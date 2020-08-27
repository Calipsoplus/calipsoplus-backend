import requests
import json
import logging
import dateutil.parser

from apprest.plugins.icat.models.calipso_experiment import CalipsoExperiment
from apprest.plugins.icat.models.calipso_session import CalipsoSession
from apprest.plugins.icat.models.calipso_investigation_user import CalipsoInvestigationUser
from calipsoplus.settings_calipso import ICAT_DATA_RETRIEVAL_ENDPOINT, ICAT_PLUGIN

icat_url = ICAT_DATA_RETRIEVAL_ENDPOINT
logger = logging.getLogger(__name__)


class ICATService:

    def get_session_id(self, access_token=None):
        try:
            # ICAT doesn't need a username as it checks if it can decrypt the token to verify the user
            session_id = json.loads(requests.post(icat_url + '/session', data={
               "plugin": ICAT_PLUGIN,
               "password": access_token
            }).text)['sessionId']

            return session_id
        except json.JSONDecodeError:
            logging.debug("Exception authenticating with ICAT service")
        return None

    def parse_data(self, data_array):
        calipso_experiments = []
        proposals = set()
        beamlines = set()

        # Multiple investigations have the same proposal_id. Get the list of proposals using a Set
        for i in range(len(data_array)):
            proposals.add(data_array[i]["Investigation"]["name"])

        for proposal in proposals:
            beamlines.clear()
            calipso_experiment = CalipsoExperiment(proposal)
            calipso_experiment.sessions = []
            experiment_abstract = ''

            for investigation in range(len(data_array)):
                if proposal == str(data_array[investigation]["Investigation"]["name"]):
                    calipso_session = CalipsoSession(data_array[investigation]["Investigation"]["id"])
                    calipso_session.start_date = \
                        dateutil.parser.parse(data_array[investigation]["Investigation"]["createTime"])
                    calipso_session.end_date = dateutil.parser.parse(
                        data_array[investigation]["Investigation"]["endDate"])
                    calipso_experiment.sessions.append(calipso_session)
                    try:
                        experiment_abstract = str(data_array[investigation]["Investigation"]["summary"])
                    except Exception:  # Some investigations don't have a summary
                        experiment_abstract = ''

                    # Add the beamline from the session to the set of beamlines for the proposal
                    beamlines.add(str(data_array[investigation]["Investigation"]["visitId"]))

            # Add all beamlines in the experiment sessions to the experiment
            # Converts a set to a string (sort of)
            calipso_experiment.beam_line = ', '.join([str(i) for i in beamlines])
            # All sessions of an experiment have the same summary. Use this summary for the proposal abstract (body)
            calipso_experiment.body = experiment_abstract
            # Add the experiment to the list of experiments
            calipso_experiments.append(calipso_experiment)

        return calipso_experiments

    def get_public_data(self, request=None):
        """
        Gets all investigations which content is public
        :return: List of CalipsoExperiment
        """
        if request.session.get('oidc_access_token', 0) is not None:
            # Get the session id (authentication)
            session_id = self.get_session_id(request.session.get('oidc_access_token', 0))
        else:
            session_id = self.get_session_id()

        # Get all of public investigation data and create python objects
        public_investigations = json.loads(requests.get(icat_url + '/catalogue/' + session_id +
                                                        '/investigation/status/released/investigation').text)

        calipso_experiments = self.parse_data(public_investigations)
        return calipso_experiments

    def get_my_investigations(self, request=None):
        """
        Gets all my investigations. Investigations that I am a participant
        :return: List of CalipsoExperiment
        """
        if request.session.get('oidc_access_token', 0) is not None:
            # Get the session id (authentication)
            session_id = self.get_session_id(request.session.get('oidc_access_token', 0))
        else:
            session_id = self.get_session_id()

        # Get all of public investigation data and create python objects
        my_investigations = json.loads(requests.get(icat_url + '/catalogue/' + session_id + '/investigation').text)

        calipso_experiments = self.parse_data(my_investigations)
        return calipso_experiments

    def get_embargo_data(self, access_token=None):
        """
        Gets all investigations that are under embargo, releaseDate > NOW
        :return: List of CalipsoExperiment
        """
        session_id = self.get_session_id(access_token)

        # Get all of embargoed investigation data and create python objects
        embargoed_investigations = json.loads(requests.get(icat_url + '/catalogue/' + session_id +
                                                           '/investigation/status/embargoed/investigation').text)

        calipso_experiments = self.parse_data(embargoed_investigations)
        return calipso_experiments

    def get_users_involved_in_investigation(self, investigation_id, request=None):
        """
        Gets users involved in an investigation
        :param request:
        :param investigation_id:
        :return: List of CalipsoInvestigationUser
        """

        if request.session.get('oidc_access_token', 0) is not None:
            # Get the session id (authentication)
            session_id = self.get_session_id(request.session.get('oidc_access_token', 0))
        else:
            session_id = self.get_session_id()

        investigation_users = json.loads(requests.get(icat_url + '/catalogue/' + session_id +
                                                      '/investigation/id/' + str(investigation_id)
                                                      + '/investigationusers').text)
        calipso_investigation_users = []

        for user in range(len(investigation_users)):
            investigation_user = CalipsoInvestigationUser()
            investigation_user.name = investigation_users[user]["name"]
            investigation_user.full_name = investigation_users[user]["fullName"]
            investigation_user.role = investigation_users[user]["role"]
            investigation_user.investigation_name = investigation_users[user]["investigationName"]
            investigation_user.investigation_id = investigation_users[user]["investigationId"]

            calipso_investigation_users.append(investigation_user)

        return calipso_investigation_users
