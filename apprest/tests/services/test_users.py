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
        request.META['HTTP_EAAHASH'] = eaa_hash
        request.META["HTTP_UID"] = uid

        json_umbrella_meta = self.user_service.get_umbrella_session_hash(request)

        self.assertEqual(json_umbrella_meta.get('uid'), uid)
        self.assertEqual(json_umbrella_meta.get('EAAHash'), eaa_hash)

    def test_lookup_none_existing_umbrella_hash(self):
        self.logger.debug('#################### test_lookup_existing_umbrella_hash ####')

        request = HttpRequest()
        request.method = 'GET'

        json_umbrella_meta = self.user_service.get_umbrella_session_hash(request)
        self.assertEqual(json_umbrella_meta, None)

    """
    def test_lookup_calipso_user_from_no_existing_hash(self):
        self.logger.debug('#################### test_lookup_calipso_user_from_no_existing_hash ####')

        eaa_hash = "b0744680-2aa3-4b12-8627-95d23e5e4af9"

        request = HttpRequest()
        request.method = 'GET'
        request.META['EAAHash'] = eaa_hash

        umbrella_hash = self.user_service.get_umbrella_session_hash(request)

        user_calipso = self.user_service.get_username_from_umbrella_hash(eaa_hash=umbrella_hash)

        self.assertTrue(user_calipso is None)

    def test_get_uo_from_existing_hash(self):
        self.logger.debug('#################### test_get_uo_from_existing_hash ####')

        # fake umbrella id

        request = HttpRequest()
        request.method = 'GET'
        request.META['EAAHash'] = 'EAAHASH'

        umbrella_hash = self.user_service.get_umbrella_session_hash(request)

        post_data = {'hash': umbrella_hash}
        headers = {'Content-type': 'application/json'}

        response = self.client.post(BACKEND_UO_EAAHASH, data=post_data, headers=headers)

        # fake response to OK and username populated
        data = {"username": "acampsm"}
        data_str = json.dumps(data)
        response.content = data_str
        response.status_code = status.HTTP_200_OK
        # fake end

        json_content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_content.get('username'), 'acampsm')

    def test_get_uo_from_non_existing_hash(self):
        self.logger.debug('#################### test_get_uo_from_non_existing_hash ####')

        # fake umbrella id
        umbrella_hash = None

        post_data = {'hash': umbrella_hash}
        headers = {'Content-type': 'application/json'}

        response = self.client.post(BACKEND_UO_EAAHASH, data=post_data, headers=headers)

        # fake response to OK and username populated
        data = {"username": None}
        data_str = json.dumps(data)
        response.content = data_str
        response.status_code = status.HTTP_404_NOT_FOUND
        # fake end

        json_content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json_content.get('username'), None)
    """


"""
    def test_get_calipso_user_from_hash(self):
        self.logger.debug('#################### test_get_uo_from_non_existing_hash ####')

        # fake umbrella id
        umbrella_hash = "hg5alk-al4jks-sn3syd-s2j1anc"

        user = self.user_service.get_username_from_umbrella_hash(eaa_hash=umbrella_hash)

        self.assertEqual(user, None)

           
            select umbrella... 
            
                login page
                returns to calipsotest     
        
           # ask for username in uo
           login(username)

           'has user in uo ? ->    yes: link'
                                   'no: register and link'

           redirect_to(settings.URL_UO_LINK)

       
                   BACKEND_UO = (end point to login service) "https://misapptest.cells.es/duo-services/login/"
                   URL_UO_LINK (to link between umbrella user and uo user)
                   URL_UO_REGISTER (to create a new user in uo)
                   URL_UMBRELLA_ID (url to Umbrella service to get session) /Shibboleth.sso/Login
       
       
                   session_umbrella = LookupUmbrellaSession('???')         # have session? 
                   if session_umbrella is None:                            # no -> go to login uo
                       DisplayLoginUO
                       no user? -> register new user in UO
                   else:                                                   # yes -> get user_from_uo
                       HASH = session_umbrella.HASH
                       user_uo = LookUpUserUO(HASH)                        # have user_from_uo?
                       if user_uo is None:                                 # no -> have uo ? 
                           Let choose:                                     # no 
                               if (user has_account in UO):
                                       show URL_UO_LINK to link account form         
                               else:
                                   call URL_UO_REGISTER to create account in uo                    #create
                                   show URL_UO_LINK to link with umbrella
                       else:
                           LoginUser()
       
                   get hash from umbrella
                   find hash in UO
                       get username from UO
"""