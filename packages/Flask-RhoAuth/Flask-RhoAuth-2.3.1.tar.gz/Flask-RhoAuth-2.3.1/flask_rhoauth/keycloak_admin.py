
from keycloak import KeycloakAdmin

from .compat import unquote


def keycloak_admin(app, client_secret=None, client_id=None):
    if not client_secret:
        client_secret = app.config['RHOAUTH_KEYCLOAK_CLIENT_ID_SECRET']

    if not client_id:
        client_id = client_id=app.config['RHOAUTH_KEYCLOAK_CLIENT_ID']

    server_url = app.config['RHOAUTH_KEYCLOAK_SERVER_URL']
    realm = unquote(app.config['RHOAUTH_OIDC_ISSUER'].split('realms/', 1)[1])

    return KeycloakAdmin(
        server_url=server_url,
        username='',
        password='',
        realm_name=realm,
        client_id=client_id,
        client_secret_key=client_secret,
        verify=True,
    )
