import logging

from rest_framework.test import testcases, APIClient
from django.contrib.auth.models import User

from rest_framework import status


class CalipsoTestCase(testcases.TestCase):
    logger = logging.getLogger(__name__)
    client = APIClient(enforce_csrf_checks=True)

    def login_and_check_http_methods(self, username, test_url, allowed_http_methods):
        self.login(username)
        self.allowed_http_methods_testing(test_url, allowed_http_methods)

    def login(self, username):
        self.logger.debug('#### Logging in as %s ####' % username)
        default_password = '12345'
        user = User.objects.get(username=username)
        user.set_password(default_password)
        user.save()
        result_login = self.client.login(username=username, password=default_password)
        self.assertTrue(result_login, 'Login incorrect for user %s' % username)

    def get_session_user(self):
        self.logger.debug('#### Getting session user ####')
        user = None
        uid = None
        if self.client.session.has_key('_auth_user_id'):
            uid = self.client.session['_auth_user_id']
            if uid:
                user = User.objects.get(pk=uid)
                self.logger.debug('#### Session user got ####')
        return user

    def logout(self):
        self.logger.debug('#### Logging out ####')
        self.client.logout()
        self.logger.debug('#### Logged out ####')

    def allowed_http_methods_testing(self, test_url, allowed_http_methods):
        self.logger.debug('#### START Testing allowed HTTP methods ####')
        self.logger.debug("%s - %s" % (test_url, str(allowed_http_methods)))
        if test_url:
            if 'GET' not in allowed_http_methods:
                response = self.client.get(test_url)
                self.assertEqual(
                    str(response.status_code),
                    str(status.HTTP_405_METHOD_NOT_ALLOWED),
                    'The response code is %s and should be %s' % (
                        response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                    )
                )
            if 'POST' not in allowed_http_methods:
                response = self.client.post(test_url)
                self.assertEqual(
                    str(response.status_code),
                    str(status.HTTP_405_METHOD_NOT_ALLOWED),
                    'The response code is %s and should be %s' % (
                        response.status_code,
                        status.HTTP_405_METHOD_NOT_ALLOWED
                    )
                )
            if 'PUT' not in allowed_http_methods:
                response = self.client.put(test_url)
                self.assertEqual(
                    str(response.status_code),
                    str(status.HTTP_405_METHOD_NOT_ALLOWED),
                    'The response code is %s and should be %s' % (
                        response.status_code,
                        status.HTTP_405_METHOD_NOT_ALLOWED
                    )
                )
            if 'DELETE' not in allowed_http_methods:
                response = self.client.delete(test_url)
                self.assertEqual(
                    str(response.status_code),
                    str(status.HTTP_405_METHOD_NOT_ALLOWED),
                    'The response code is %s and should be %s' % (
                        response.status_code,
                        status.HTTP_405_METHOD_NOT_ALLOWED
                    )
                )
            if 'HEAD' not in allowed_http_methods:
                response = self.client.head(test_url)
                self.assertEqual(
                    str(response.status_code),
                    str(status.HTTP_405_METHOD_NOT_ALLOWED),
                    'The response code is %s and should be %s' % (
                        response.status_code,
                        status.HTTP_405_METHOD_NOT_ALLOWED
                    )
                )
            if 'OPTIONS' not in allowed_http_methods:
                response = self.client.options(test_url)
                self.assertEqual(
                    str(response.status_code),
                    str(status.HTTP_405_METHOD_NOT_ALLOWED),
                    'The response code is %s and should be %s' % (
                        response.status_code,
                        status.HTTP_405_METHOD_NOT_ALLOWED
                    )
                )
            if 'PATCH' not in allowed_http_methods:
                response = self.client.patch(test_url)
                self.assertEqual(
                    str(response.status_code),
                    str(status.HTTP_405_METHOD_NOT_ALLOWED),
                    'The response code is %s and should be %s' % (
                        response.status_code,
                        status.HTTP_405_METHOD_NOT_ALLOWED
                    )
                )
        self.logger.debug('#### END Testing allowed HTTP methods ####')