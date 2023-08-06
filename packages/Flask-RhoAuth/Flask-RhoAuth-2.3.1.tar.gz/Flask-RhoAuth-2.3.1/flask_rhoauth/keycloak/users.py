import json
import logging
import time
from typing import List, Optional

from keycloak import KeycloakGetError

from .exceptions import KeycloakConflictError
from .service import KeycloakService
from .types import UserRepresentation, QueryDict

logger = logging.getLogger(__name__)


class UserService(KeycloakService):
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
        super().__init__(app)

    def create(self,
               user: UserRepresentation,
               roles: List[str] = None,
               update_password: bool = False,
               verify_email: bool = False) -> UserRepresentation:

        if 'requiredActions' not in user:
            user['requiredActions'] = []

        username = user["username"]

        if update_password:
            user['requiredActions'].append("UPDATE_PASSWORD")
        if verify_email:
            user['requiredActions'].append("VERIFY_EMAIL")

        # account has to be enabled if we're sending emails to the user
        if update_password or verify_email:
            user['enabled'] = True

        uid = self._admin.create_user(user)
        if isinstance(uid, (bytes, bytearray)):
            uid = uid.decode()

        # if user already exists, the uid is returned
        if uid != "":
            raise KeycloakConflictError(username)

        # sleep here because we might be too fast to get the new
        # user and not all keycloak servers may be in sync
        time.sleep(0.1)

        user = self.get(username=username)
        uid = user["id"]

        if roles is not None and len(roles) > 0:
            self.set_roles(uid, roles)
            # we've added roles, get an updated user representation
            user = self.get(uid)

        if verify_email or update_password:
            self._admin.send_verify_email(uid)

        return user

    def update(self, user: UserRepresentation) -> UserRepresentation:
        """
        Update given keys for a user.

        If attributes key is given, all old attributes will be overwritten!!!!
        :param user:
        :return:
        """
        uid = user["id"]
        self._admin.update_user(uid, user)
        return self.get(uid)

    def set_roles(self, uid: str, roles: List[str]) -> bool:
        """
        Set roles for a user.
        This method will overwrite all roles currently given to the user.
        :param uid:
        :param roles:
        :return:
        """
        client_id = self._get_client_uid()
        client_roles = self._admin.get_client_roles(client_id)
        client_roles_by_name = {
            r['name']: r for r in client_roles
        }

        roles = [client_roles_by_name[r] for r in roles]

        try:
            self._admin.delete_client_roles_of_user(uid, client_id, roles)
            self._admin.assign_client_role(uid, client_id, roles)
            return True
        except KeycloakGetError as e:
            return False

    def get_roles(self, uid: str) -> List[str]:
        """
        Get the list of role names for the given UID for this Client-ID
        :param uid:
        :return:
        """
        roles = self._admin.get_client_roles_of_user(
            uid, self._get_client_uid()
        )
        return [r["name"] for r in roles]

    def delete(self, uid: str) -> bool:
        """
        Delete a user from this realm.
        :param uid:
        :return: True if successfully deleted, false if an error occurred.
        """
        return self._get_success(
            lambda: self._admin.delete_user(uid)
        )

    def get(self, uid: str = None, username: str = None) -> \
            Optional[UserRepresentation]:
        """
            Get a user representation by UID or Username
        :param uid:
        :param username:
        :return:
        """

        if uid is not None:
            return self._admin.get_user(uid)

        if username is not None:
            users = self.get_users(query={"username": username})
            return next(
                (user for user in users if user["username"] == username), None
            )

        logger.warning("uid or username not specified in UserService::get")
        return None

    def get_users(self, query: QueryDict = None) -> List[UserRepresentation]:
        """
        :param query: key value pairs of user attributes to search against along
                      with pagination options
                       email, firstName, lastName,
                       search (A String contained in username, first or
                       last name, or email), username

                       first (int), max (int)
        :return:
        """
        if query is None:
            query = {}

        return self._admin.get_users(query)

    def set_password(self, uid: str, password, temporary=False):
        """
        Set a permanent or temporary password for the given UID
        :param uid:
        :param password:
        :param temporary:
        :return: True if successful, False if any error received
        """
        return self._get_success(
            lambda: self._admin.set_user_password(uid, password, temporary)
        )

    def reset_password(self, uid: str):
        """
        Send a reset password email to the given UID
        :param uid:
        :return: True if successful, False if any error received
        """
        return self._get_success(
            lambda: self._admin.send_update_account(
                uid, payload=json.dumps(['UPDATE_PASSWORD'])
            )
        )
