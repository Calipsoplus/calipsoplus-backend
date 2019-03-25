from mozilla_django_oidc.auth import OIDCAuthenticationBackend


def generate_username(username):
    return username


"""
Custom OpenID Connect Authentication class.
Used to populate user object with more data using claims offered by the OpenID Connect provider.
Provides creation of new user and updating of current users
"""


class MyOIDCAB(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(MyOIDCAB, self).create_user(claims)

        user.first_name = claims.get('given_name', '')
        user.username = claims.get('preferred_username', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.username = claims.get('preferred_username', '')
        user.save()

        return user
