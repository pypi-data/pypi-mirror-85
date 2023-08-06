from typing import Callable

from keycloak import KeycloakGetError

from ..keycloak_admin import keycloak_admin


class KeycloakService:
    def __init__(self, app):
        """

        :param app: flask_app with the available keys to init keycloak admin.
                    required keys w/ examples:
                    RHOAUTH_KEYCLOAK_CLIENT_ID=prra-realm-mgmt
                    RHOAUTH_KEYCLOAK_CLIENT_ID_SECRET=8675309-35f6-4c5b-9777-aaaaaaaaaaaa
                    RHOAUTH_KEYCLOAK_SERVER_URL=https://keycloak.example.com/auth/
                    RHOAUTH_OIDC_ISSUER=https://keycloak.example.com/auth/realms/prra
                    RHOAUTH_OIDC_CLIENT_ID=prra-prod
        """
        self._app = app
        self._admin = keycloak_admin(app)
        self._client_id = self._app.config['RHOAUTH_OIDC_CLIENT_ID']
        self._client_uid = None

    def _get_client_uid(self) -> str:
        """
        Get the actual client uid (not name id) for this keycloak realm-mgmt
        instance
        :return: client_uid
        """
        if self._client_uid is not None:
            return self._client_uid

        self._client_uid = self._admin.get_client_id(self._get_client_id())
        return self._client_uid

    def _get_client_id(self) -> str:
        """
        Get the client id (name) for this keycloak realm-mgmt instance
        :return: client_id
        """
        return self._client_id

    @staticmethod
    def _get_success(fn: Callable, err_cls=KeycloakGetError):
        try:
            fn()
            return True
        except err_cls as e:
            return False
