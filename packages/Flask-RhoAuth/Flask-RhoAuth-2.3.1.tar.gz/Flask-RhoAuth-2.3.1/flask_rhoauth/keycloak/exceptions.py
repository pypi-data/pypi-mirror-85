from keycloak.exceptions import KeycloakError


class KeycloakConflictError(KeycloakError):
    def __init__(self, msg: str):
        KeycloakError.__init__(self, msg, 409, None)
