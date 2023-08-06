__version__ = '2.3.1'


try:
    from .openid import OpenIDConnect, OpenIDUser, current_user
except:
    OpenIDConnect = None
    OpenIDUser = None
    current_user = None

try:
    from keycloak import KeycloakOpenID, KeycloakAdmin
    from .keycloak_admin import keycloak_admin
except:
    KeycloakOpenID = None
    KeycloakAdmin = None
    keycloak_admin = None

try:
    from .api_auth import Consumer, ApiKey, get_api_key
except:
    Consumer = None
    ApiKey = None
    get_api_key = None
