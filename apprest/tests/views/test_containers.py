import json
from django.urls import reverse
from rest_framework import status

import logging

from apprest.models.user import CalipsoUser
from apprest.services.quota import CalipsoUserQuotaServices
from apprest.tests.utils import CalipsoTestCase

logger = logging.getLogger(__name__)


class ContainerViewsTestCase(CalipsoTestCase):
    logger = logging.getLogger(__name__)
    fixtures = ['users.json', 'images.json', 'quotas.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.scientist_1 = CalipsoUser.objects.get(pk=1)
        self.quota_service = CalipsoUserQuotaServices()
        self.logger.debug('#### setUp END ####')

    def test_view_run_stop_rm_container(self):
        self.logger.debug('#### TEST test_view_run_stop_rm_container START ####')

        base_url = '/container/list/%s/'

        # Not authenticated -> 403
        url = base_url % self.scientist_1.user.username

        # Login and check methods
        self.login_and_check_http_methods(self.scientist_1.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        # run
        response_run = self.client.get(reverse('run_container',
                                               kwargs={'username': 'userA', 'experiment': 'EXPERIMENT_SN',
                                                       'public_name': 'base_jupyter'}))
        self.assertEqual(response_run.status_code, status.HTTP_201_CREATED)

        json_content = json.loads(response_run.content.decode("utf-8"))

        container_name = json_content['container_name']

        # stop
        response_stop = self.client.get(
            reverse('stop_container', kwargs={'username': 'userA', 'container_name': container_name}))
        self.assertEqual(response_stop.status_code, status.HTTP_200_OK)

        # remove
        response_rm = self.client.get(
            reverse('rm_container', kwargs={'username': 'userA', 'container_name': container_name}))
        self.assertEqual(response_rm.status_code, status.HTTP_200_OK)

        self.logger.debug('#### TEST test_view_run_stop_rm_container END ####')

    def test_user_HTTP_403_FORBIDDEN(self):
        self.logger.debug('#### TEST test_user_HTTP_403_FORBIDDEN START ####')

        response_run = self.client.get(reverse('run_container',
                                               kwargs={'username': 'userA', 'experiment': 'EXPERIMENT_SN',
                                                       'public_name': 'base_jupyter'}))
        self.assertEqual(response_run.status_code, status.HTTP_403_FORBIDDEN)

        self.logger.debug('#### TEST test_user_HTTP_403_FORBIDDEN END ####')

    def test_max_MAX_CONTAINER_PER_USER_containers_active_per_user(self):
        self.logger.debug('#### TEST test_max_MAX_CONTAINER_PER_USER_containers_active_per_user START ####')

        base_url = '/container/list/%s/'

        url = base_url % self.scientist_1.user.username

        # Login and check methods
        self.login_and_check_http_methods(self.scientist_1.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        all_container_responses = []

        quota = self.quota_service.get_default_quota(username=self.scientist_1.user.username)
        logger.info("MAX SIM:" + str(quota.max_simultaneous))

        for x in range(0, quota.max_simultaneous):
            all_container_responses.append(self.client.get(
                reverse('run_container',
                        kwargs={'username': 'userA', 'experiment': 'EXPERIMENTS', 'public_name': 'base_jupyter'})))
            self.assertEqual(all_container_responses[x].status_code, status.HTTP_201_CREATED)

        last_fail_container = self.client.get(
            reverse('run_container',
                    kwargs={'username': 'userA', 'experiment': 'EXPERIMENT_LAST', 'public_name': 'base_jupyter'}))

        self.assertEqual(last_fail_container.status_code, status.HTTP_204_NO_CONTENT)

        # stop and remove all
        for x in range(0, quota.max_simultaneous):
            self.stop_remove_container(container_response=all_container_responses.pop(), username='userA')

        self.logger.debug('#### TEST max_3_containers_active_per_user END ####')

    def stop_remove_container(self, container_response, username):
        # stop
        json_content = json.loads(container_response.content.decode("utf-8"))
        container_name = json_content['container_name']

        response_stop = self.client.get(
            reverse('stop_container', kwargs={'username': username, 'container_name': container_name}))
        self.assertEqual(response_stop.status_code, status.HTTP_200_OK)

        # remove
        response_rm = self.client.get(
            reverse('rm_container', kwargs={'username': username, 'container_name': container_name}))
        self.assertEqual(response_rm.status_code, status.HTTP_200_OK)

    def test_read_logs_from_container(self):

        self.logger.debug('#### TEST test_read_logs_from_container START ####')
        base_url = '/container/list/%s/'

        # Not authenticated -> 403
        url = base_url % self.scientist_1.user.username

        # Login and check methods
        self.login_and_check_http_methods(self.scientist_1.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        # run
        response_run = self.client.get(reverse('run_container',
                                               kwargs={'username': 'userA', 'experiment': 'EXPERIMENT_SN',
                                                       'public_name': 'base_jupyter'}))

        self.assertEqual(response_run.status_code, status.HTTP_201_CREATED)

        self.stop_remove_container(container_response=response_run, username='userA')

        self.logger.debug('#### TEST test_read_logs_from_container END ####')


    def test_own_resources_container(self):
        self.logger.debug('#### TEST test_own_resources_container START ####')

        base_url = '/container/list/%s/'

        # Not authenticated -> 403
        url = base_url % self.scientist_1.user.username

        # Login and check methods
        self.login_and_check_http_methods(self.scientist_1.user.username, url, ['GET', 'HEAD', 'OPTIONS'])

        # run
        response_run = self.client.get(reverse('run_container',
                                               kwargs={'username': 'userA', 'experiment': 'userA',
                                                       'public_name': 'base_jupyter'}))
        self.assertEqual(response_run.status_code, status.HTTP_201_CREATED)

        json_content = json.loads(response_run.content.decode("utf-8"))

        container_name = json_content['container_name']

        # stop
        response_stop = self.client.get(
            reverse('stop_container', kwargs={'username': 'userA', 'container_name': container_name}))
        self.assertEqual(response_stop.status_code, status.HTTP_200_OK)

        # remove
        response_rm = self.client.get(
            reverse('rm_container', kwargs={'username': 'userA', 'container_name': container_name}))
        self.assertEqual(response_rm.status_code, status.HTTP_200_OK)

        self.logger.debug('#### TEST test_own_resources_container END ####')