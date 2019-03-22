import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

import logging

from apprest.services.quota import CalipsoUserQuotaServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ResourceViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'images.json', 'quotas.json']

    def setUp(self):
        self.logger.debug('#### setUp ResourceViewsTestCase START ####')
        self.scientist = User.objects.get(pk=1)
        self.quota_service = CalipsoUserQuotaServices()
        self.logger.debug('#### setUp ResourceViewsTestCase END ####')

    def test_view_run_stop_rm_resource(self):
        self.logger.debug('#### TEST test_view_run_stop_rm_resource START ####')

        username = self.scientist.username

        base_url = '/resource/list/%s/'
        url = base_url % username

        # Login and check methods
        self.login_and_check_http_methods(username, url, ['GET', 'HEAD', 'OPTIONS'])

        # run
        response_run = self.client.get(reverse('run_resource',
                                               kwargs={'username': username,
                                                       'experiment': 'EXPERIMENT_SN',
                                                       'public_name': 'base_jupyter'}))

        self.assertEqual(response_run.status_code, status.HTTP_201_CREATED)

        json_content = json.loads(response_run.content.decode("utf-8"))

        resource_name = json_content['container_name']

        # stop
        response_stop = self.client.get(
            reverse('stop_resource', kwargs={'username': 'userA', 'resource_name': resource_name,
                                             'public_name': 'base_jupyter'}))
        self.assertEqual(response_stop.status_code, status.HTTP_200_OK)

        # remove
        response_rm = self.client.get(
            reverse('rm_resource', kwargs={'username': 'userA', 'resource_name': resource_name,
                                           'public_name': 'base_jupyter'}))
        self.assertEqual(response_rm.status_code, status.HTTP_200_OK)

        self.logger.debug('#### TEST test_view_run_stop_rm_resource END ####')

    def test_max_MAX_RESOURCES_PER_USER_active(self):
        self.logger.debug('#### TEST test_max_MAX_RESOURCES_PER_USER_active START ####')

        base_url = '/resource/list/%s/'

        username = self.scientist.username

        url = base_url % username

        # Login and check methods
        self.login_and_check_http_methods(username, url, ['GET', 'HEAD', 'OPTIONS'])

        all_resource_responses = []

        quota = self.quota_service.get_default_quota(username=username)
        logger.info("MAX SIM:" + str(quota.max_simultaneous))

        for x in range(0, quota.max_simultaneous):
            all_resource_responses.append(self.client.get(
                reverse('run_resource',
                        kwargs={'username': username, 'experiment': 'EXPERIMENTS%d' % x,
                                'public_name': 'base_jupyter'})))
            self.assertEqual(all_resource_responses[x].status_code, status.HTTP_201_CREATED)

        last_fail_resource = self.client.get(
            reverse('run_resource',
                    kwargs={'username': username, 'experiment': 'EXPERIMENT_LAST', 'public_name': 'base_jupyter'}))

        self.assertEqual(last_fail_resource.status_code, status.HTTP_204_NO_CONTENT)

        # stop and remove all
        for x in range(0, quota.max_simultaneous):
            self.stop_remove_resource(resource_response=all_resource_responses.pop(), username=username,
                                      public_name='base_jupyter')

        self.logger.debug('#### TEST test_max_MAX_RESOURCES_PER_USER_active END ####')

    def stop_remove_resource(self, resource_response, username, public_name):
        # stop
        json_content = json.loads(resource_response.content.decode("utf-8"))
        resource_name = json_content['container_name']

        response_stop = self.client.get(
            reverse('stop_resource',
                    kwargs={'username': username, 'resource_name': resource_name, 'public_name': public_name}))
        self.assertEqual(response_stop.status_code, status.HTTP_200_OK)

        # remove
        response_rm = self.client.get(
            reverse('rm_resource',
                    kwargs={'username': username, 'resource_name': resource_name, 'public_name': public_name}))
        self.assertEqual(response_rm.status_code, status.HTTP_200_OK)
