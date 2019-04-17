import requests
import json

import dateutil.parser

from apprest.plugins.icat.models.calipso_experiment import CalipsoExperiment
from apprest.plugins.icat.models.calipso_session import CalipsoSession
from calipsoplus.settings_calipso import ICAT_DATA_RETRIEVAL_ENDPOINT, ICAT_PASSWORD, ICAT_PLUGIN, ICAT_USERNAME


def get_embargo_data():
    icat_url = ICAT_DATA_RETRIEVAL_ENDPOINT

    session_id = json.loads(requests.post(icat_url + '/session', data={
        "plugin": ICAT_PLUGIN,
        "username": ICAT_USERNAME,
        "password": ICAT_PASSWORD
        }).text)['sessionId']
    embargoed = json.loads(requests.get(icat_url + '/catalogue/' + session_id +
                                        "/investigation/status/embargoed/investigation").text)
    calipso_experiments = []
    proposals = set()
    beamlines = set()

    # Multiple investigations have the same proposal_id. Get the list of proposals using a Set
    for i in range(len(embargoed)):
        proposals.add(embargoed[i]["Investigation"]["name"])

    for proposal in proposals:
        beamlines.clear()
        calipso_experiment = CalipsoExperiment(proposal)
        calipso_experiment.sessions = []
        experiment_abstract = ''

        for investigation in range(len(embargoed)):
            if proposal == str(embargoed[investigation]["Investigation"]["name"]):
                calipso_session = CalipsoSession(embargoed[investigation]["Investigation"]["id"])
                calipso_session.start_date = \
                    dateutil.parser.parse(embargoed[investigation]["Investigation"]["createTime"])
                calipso_session.end_date = dateutil.parser.parse(embargoed[investigation]["Investigation"]["endDate"])
                calipso_experiment.sessions.append(calipso_session)
                try:
                    experiment_abstract = str(embargoed[investigation]["Investigation"]["summary"])
                except Exception:  # Some investigations don't have a summary
                    experiment_abstract = ''

                # Add the beamline from the session to the set of beamlines for the proposal
                beamlines.add(str(embargoed[investigation]["Investigation"]["visitId"]))

        # Add all beamlines in the experiment sessions to the experiment
        # Converts a set to a string (sort of)
        calipso_experiment.beam_line = ', '.join([str(i) for i in beamlines])
        # All sessions of an experiment have the same summary. Use this summary for the proposal abstract (body)
        calipso_experiment.body = experiment_abstract
        # Add the experiment to the list of experiments
        calipso_experiments.append(calipso_experiment)

    return calipso_experiments

