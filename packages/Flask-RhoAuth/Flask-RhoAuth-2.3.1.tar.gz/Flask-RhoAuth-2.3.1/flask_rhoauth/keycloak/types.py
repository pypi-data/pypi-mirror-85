from typing import Dict

# For now, we'll user a generic Dict type for Keycloak models.
# once we support Python3.8, we can use TypeDict to explicitly define keys.
# https://docs.python.org/3.8/library/typing.html#typing.TypedDict


# https://www.keycloak.org/docs-api/6.0/rest-api/index.html#_map
Map = Dict[str, any]

QueryDict = Dict[str, any]
# "username": str
# "email": str
# "firstName": str
# "lastName": str
# "first": int
# "max": int # Maximum results size (defaults to 100)
# "search": str # A String contained in username, first or last name, or email
# "briefRepresentation": bool # return few values of user

# https://www.keycloak.org/docs-api/6.0/rest-api/index.html#_userconsentrepresentation
UserConsentRepresentation = Dict[str, any]
# "clientId": str
# "createdDate": int
# "grantedClientScopes": List[str]
# "lastUpdatedDate": int

# https://www.keycloak.org/docs-api/6.0/rest-api/index.html#_multivaluedhashmap
MultivaluedHashMap = Dict[str, any]
# "empty": bool
# "loadFactor": float
# "threshold": int

# https://www.keycloak.org/docs-api/6.0/rest-api/index.html#_federatedidentityrepresentation
FederatedIdentityRepresentation = Dict[str, any]
# "identityProvider": str
# "userId": str
# "userName": str

# https://www.keycloak.org/docs-api/6.0/rest-api/index.html#_credentialrepresentation
CredentialRepresentation = Dict[str, any]


# "algorithm": str
# "config": MultivaluedHashMap
# "counter": int
# "createdDate": int
# "device": str
# "digits": int
# "hashIterations": int
# "hashedSaltedValue": str
# "period": int
# "salt": str
# "temporary": bool
# "type": str
# "value": str

def user_has_attr(user, attr_name):
    return user is not None \
           and 'attributes' in user \
           and attr_name in user['attributes']


def get_user_attr(user, attr_name, default_value):
    attr = default_value
    if not user_has_attr(user, attr_name):
        return attr

    # attributes are stored as csv in Keycloak,
    # but it's possible to send a dict to Keycloak.
    # handle both cases
    attr_vals = user['attributes'][attr_name]
    if isinstance(attr_vals, str):
        attr_vals = [attr_vals]

    return attr_vals[0]


def set_user_attr(user, attr_name, value):
    if 'attributes' not in user:
        user['attributes'] = {}

    user['attributes'][attr_name] = value


# https://www.keycloak.org/docs-api/6.0/rest-api/index.html#_userrepresentation
UserRepresentation = Dict[str, any]

# "access": Map
# "attributes": Map
# "clientConsents": List[UserConsentRepresentation]
# "clientRoles": Map
# "createdTimestamp": int
# "credentials": List[CredentialRepresentation]
# "disableableCredentialTypes": List[str]
# "email": str
# "emailVerified": bool
# "enabled": bool
# "federatedIdentities": List[FederatedIdentityRepresentation]
# "federationLink": str
# "firstName": str
# "groups": List[str]
# "id": str
# "lastName": str
# "notBefore": int
# "origin": str
# "realmRoles": List[str]
# "requiredActions": List[str]
# "self": str
# "serviceAccountClientId": str
# "username": str
