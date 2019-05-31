#OpenID Connect
OpenID Connect (OIDC) is an authentication layer on top of OAuth 2.0, an authorization framework.
The standard is controlled by the OpenID Foundation.   

OIDC can be enabled as an authentication method for the portal. 

##Keycloak Requirement  
Keycloak will need to return the username after the user has been authenticated.

##Settings
To enable OpenID Connect, modify the settings in the settings.py. The default values should
look similar to this:

``` python 
# Open ID Connect Enabled
OIDC_ENABLED = False
# Open ID Connect credentials
OIDC_RP_CLIENT_ID = ''
OIDC_RP_CLIENT_SECRET = ''
OIDC_OP_AUTHORIZATION_ENDPOINT = '../auth'
OIDC_OP_TOKEN_ENDPOINT = '../token'
OIDC_OP_USER_ENDPOINT = '../userinfo'
OIDC_OP_JWKS_ENDPOINT = '../certs'
OIDC_RP_SIGN_ALGO = ''  # RS256 or HS256 (check your provider)
```
To enable Open ID Conenct, change OIDC_ENABLED to True  
Change the defualt values to the values which are provided in Keycloak. The following
variables must also be set and will depend on your portal setup.

```python
# URL to the front end experiment page. After the user has authenticated, they will be redirected to this page in the
# frontend
REDIRECT_AFTER_OIDC_URL = 'http://frontend.fr/navigation'

# URL to the calipsoplus home page. After the user has logged out, they should be redirected here. (Does not require
# authentication)
LOGOUT_REDIRECT_URL = 'http://frontend.fr'
```

After the user has authenticated, they will need to be redirected back to the portal.
Modify the REDIRECT_AFTER_OIDC_URL variable so that it has either the ip address or the URL
of the frontend server. /navigation should remain as this is the page the user will be directed to.  

When the user logs out, they will need to be directed to a part of the portal which does not
require authentication.  
Modify LOGOUT_REDIRECT_URL to the ip adddress or the URL of the frontend server.