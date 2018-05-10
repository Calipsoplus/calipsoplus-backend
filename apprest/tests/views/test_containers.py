import json
import pdb

from django.urls import reverse
from rest_framework import status

import logging

from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ContainerViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.logger.debug('#### setUp END ####')

    def test_view_run_stop_rm_container(self):
        self.logger.debug('#### TEST test_view_run_stop_rm_container START ####')

        # run
        response_run = self.client.post(reverse('run_container',
                                                kwargs={'username': 'acampsm', 'experiment': 'EXPERIMENT_SN'}))
        self.assertEqual(response_run.status_code, status.HTTP_201_CREATED)

        json_content = json.loads(response_run.content.decode("utf-8"))

        container_name = json_content['container_name']

        # stop
        response_stop = self.client.get(reverse('stop_container', kwargs={'container_name': container_name}))
        self.assertEqual(response_stop.status_code, status.HTTP_200_OK)

        # remove
        response_rm = self.client.get(reverse('rm_container', kwargs={'container_name': container_name}))
        self.assertEqual(response_rm.status_code, status.HTTP_200_OK)

        self.logger.debug('#### TEST test_view_run_stop_rm_container END ####')