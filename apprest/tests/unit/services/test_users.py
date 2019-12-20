import json

from django.http import HttpRequest

from apprest.services.user import CalipsoUserServices
from apprest.tests.utils import CalipsoTestCase


class UserServiceTestCase(CalipsoTestCase):

    def setUp(self):
        self.logger.debug('#################### setup test UserServiceTestCase  ####')
        self.user_service = CalipsoUserServices()

    def test_lookup_existing_umbrella_hash(self):
        self.logger.debug('#################### test_lookup_existing_umbrella_hash ####')

        eaa_hash = "b0744680-2aa3-4b12-8627-95d23e5e4af9"
        uid = "eibarz"

        request = HttpRequest()
        request.method = 'GET'
        #request.META['HTTP_EAAHASH'] = eaa_hash
        #request.META["HTTP_UID"] = uid
        request.META['EAAHash'] = eaa_hash
        request.META["uid"] = uid

        json_umbrella_meta = self.user_service.get_umbrella_session_hash(request)

        self.assertEqual(json_umbrella_meta.get('uid'), uid)
        self.assertEqual(json_umbrella_meta.get('EAAHash'), eaa_hash)

    def test_lookup_none_existing_umbrella_hash(self):
        self.logger.debug('#################### test_lookup_existing_umbrella_hash ####')

        request = HttpRequest()
        request.method = 'GET'

        json_umbrella_meta = self.user_service.get_umbrella_session_hash(request)
        self.assertEqual(json_umbrella_meta, None)

