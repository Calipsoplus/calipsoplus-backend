import json

from django.urls import reverse
from rest_framework import status

from apprest.models import CalipsoUser
from apprest.services.container import CalipsoContainersServices
from apprest.tests.utils import CalipsoTestCase


class ContainerViewsTestCase(CalipsoTestCase):
    fixtures = ['users.json', 'containers.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.service = CalipsoContainersServices()
        self.scientist_1 = CalipsoUser.objects.get(pk=1)

        self.logger.debug('#### setUp END ####')

    def test_get_all_containers(self):
        self.logger.debug('#### TEST test_get_all_containers START ####')

        username = self.scientist_1.user.username

        base_url = '/resource/list/%s/'
        url = base_url % username

        self.login_and_check_http_methods(username, url, ['GET', 'HEAD', 'OPTIONS'])

        self.logger.debug('# TEST URL --> %s' % url)

        response = self.client.get(reverse('list_resource', kwargs={'username': username}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_content = json.loads(response.content.decode("utf-8"))

        self.assertIsInstance(json_content, list)
        self.assertEqual(len(json_content), 2)

        self.logger.debug('#### TEST test_get_all_containers END ####')
