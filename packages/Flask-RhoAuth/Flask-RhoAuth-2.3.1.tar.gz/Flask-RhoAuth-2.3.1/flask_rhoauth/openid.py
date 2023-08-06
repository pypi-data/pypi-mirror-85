import logging
import os
import requests

from datetime import datetime
from functools import wraps

from flask import (
    session, url_for, redirect, request, g, abort, current_app, Response
)
from jwkest import jws, jwk, jwt
from requests_oauthlib import OAuth2Session
from werkzeug.local import LocalProxy
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError


from .utils.string import rndstr
from .compat import PY2

logger = logging.getLogger(__name__)


current_user = LocalProxy(lambda: _get_user())


def get_access_token_from_request(signature_keys):
    """
    :param signature_keys:
    :return: b64 encoded access_token
    :rtype str
    """
    token = None
    if 'Authorization' in request.headers and\
            request.headers['Authorization'].startswith('Bearer '):
        token = request.headers['Authorization'].split(None,1)[1].strip()
    if 'access_token' in request.form:
        token = request.form['access_token']
    elif 'access_token' in request.args:
        token = request.args['access_token']

    if not token:
        return None

    # Validate the token to make sure we didn't get anything funky
    try:
        _jws = jws.JWS()
        _jws.verify_compact(token, keys=signature_keys, sigalg='RS256')
        access_token = _jws.jwt.payload()
    except Exception as e:
        logger.exception(e)
        return None

    if OpenIDConnect.validate_token_claims(access_token, verify_iss=False,
                                           verify_aud=False, verify_exp=True):
        return token
    return None


def secure_url_for(endpoint):
    """ Returns a https url for the given endpoint. If variable
        OAUTHLIB_INSECURE_TRANSPORT is set, then it uses http
    """
    if os.getenv('OAUTHLIB_INSECURE_TRANSPORT'):
        logger.info("INSECURE")
        return url_for(endpoint, _external=True)
    logger.info("SECURE")
    return url_for(endpoint, _external=True, _scheme='https')


class OpenIDConnect(object):

    EXTENSION_NAME = 'flask_rhoauth'

    def __init__(self, app=None):
        self._on_login_funcs = []
        self._on_logout_funcs = []
        self._on_token_refresh_funcs = []

        if app:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('RHOAUTH_OIDC_SCOPES', ['openid'])
        app.config.setdefault('RHOAUTH_OIDC_OPENID_REALM', None)
        app.config.setdefault('RHOAUTH_OIDC_CLIENT_ID', None)
        app.config.setdefault('RHOAUTH_OIDC_ISSUER', None)
        app.config.setdefault('RHOAUTH_OIDC_REDIRECT_URI', '/oidc_auth_cb')
        app.config.setdefault('RHOAUTH_OIDC_LOGOUT_URI', '/oidc_logout_cb')
        app.config.setdefault('RHOAUTH_OIDC_AUTH_ENDPOINT', None)
        app.config.setdefault('RHOAUTH_OIDC_TOKEN_ENDPOINT', None)
        app.config.setdefault('RHOAUTH_OIDC_JWKS_URI_ENDPOINT', None)
        app.config.setdefault('RHOAUTH_OIDC_END_SESSION_ENDPOINT', None)
        app.config.setdefault('RHOAUTH_OIDC_END_SESSION_REDIRECT_URI', '/')
        app.config.setdefault('RHOAUTH_OIDC_USER_CLASS', OpenIDUser)
        app.config.setdefault('RHOAUTH_KEYCLOAK_SERVER_URL', None)

        # Hooks for loading/unloading tokens from session
        app.before_request(self._before_request)
        app.after_request(self._after_request)

        # Add the redirect route
        app.route(app.config['RHOAUTH_OIDC_REDIRECT_URI'])(self._auth_callback)
        app.route(app.config['RHOAUTH_OIDC_LOGOUT_URI'])(self._logout_callback)

        # Load certificates for verifying tokens
        self.keys = []
        self._load_keys(app.config['RHOAUTH_OIDC_JWKS_URI_ENDPOINT'])

        self._error_view = None

        app.context_processor(_user_context_processor)

        # Register extesion in app
        app.extensions[self.EXTENSION_NAME] = self

    def require_login(self, view_fn, roles=[]):

        """
            Decorator that should be used for routes that render content
        """
        @wraps(view_fn)
        def decorated(*args, **kwargs):
            if hasattr(g, 'oidc_id_token') and g.oidc_id_token:
                if roles and not self._has_permissions(g.oidc_access_token,
                                                       roles):
                    self._handle_error_response(status_code=401)
                return view_fn(*args, **kwargs)

            return self._authenticate()
        return decorated

    def require_permission(self, roles=[]):
        """
            Decorator that should be used for routes that return data
        """
        def wrapper(view_fn):
            @wraps(view_fn)
            def decorated(*args, **kwargs):
                # Get access token from session or request
                access_token = None
                if hasattr(g, 'oidc_access_token') and g.oidc_access_token:
                    access_token = g.oidc_access_token
                else:
                    _access_token = get_access_token_from_request(self.keys)
                    if _access_token:
                        access_token = jwt.JWT().unpack(_access_token).payload()

                # Retur 401 if we don't have an access token
                if not access_token:
                    return self._handle_error_response(status_code=401)

                # Return 401 if access token has expired
                if not self.validate_token_claims(access_token,
                        verify_iss=False,verify_aud=False, verify_exp=True):
                    return self._handle_error_response(status_code=401)

                # Return 401 if no permissions
                if not self._has_permissions(access_token, roles):
                    return self._handle_error_response(status_code=401)

                # If all checks above passed, the allow through
                return view_fn(*args, **kwargs)

            return decorated
        return wrapper

    def _load_keys(self, jwks_uri_endpoint):
        res = requests.get(jwks_uri_endpoint)
        for key in res.json()['keys']:
            self.keys.append(jwk.RSAKey(**key))

    def _has_permissions(self, access_token, roles=[]):
        client_id = current_app.config['RHOAUTH_OIDC_CLIENT_ID']
        access_roles = access_token['resource_access']\
            .get(client_id, {})\
            .get('roles', [])
        for role in roles:
            if role in access_roles:
                return True
        return False

    def _before_request(self):
        id_token = session.get('id_token')
        access_token = session.get('access_token')
        refresh_token = session.get('refresh_token')
        g.oidc_id_token = None
        g.oidc_access_token = None

        if not id_token:
            return

        _jwt = jwt.JWT()
        _id_token = _jwt.unpack(id_token).payload()
        _access_token = _jwt.unpack(access_token).payload()

        if not self.validate_token_claims(_id_token, verify_iss=False,
                                          verify_aud=False, verify_exp=True):
            self._refresh_tokens(refresh_token)
        else:
            g.oidc_id_token = _id_token
            g.oidc_access_token = _access_token

    def _after_request(self, response):
        g.oidc_id_token = None
        g.oidc_access_token = None
        return response

    def _set_session_token(self, id_token, access_token, refresh_token):
        session['id_token'] = id_token
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token

    def _clear_session(self):
        session.pop('id_token')
        session.pop('access_token')
        session.pop('refresh_token')
        session.pop('state')
        session.pop('nonce')

    def authenticate(self):
        return self._authenticate()

    def _authenticate(self):
        # Creates the authentication request that redirects the user to
        # the provider's login page
        auth = OAuth2Session(
            client_id=current_app.config['RHOAUTH_OIDC_CLIENT_ID'],
            redirect_uri=secure_url_for('_auth_callback'),
            scope=current_app.config['RHOAUTH_OIDC_SCOPES']
        )

        session['return_url'] = request.url
        session['state'] = rndstr()
        session['nonce'] = rndstr()
        authorization_url, state = auth.authorization_url(
            current_app.config['RHOAUTH_OIDC_AUTH_ENDPOINT'],
            state=session['state'],
            nonce=session['nonce']
        )

        return redirect(authorization_url)

    def _auth_callback(self):
        # Obtain the id_token, access_token and refresh token
        client = OAuth2Session(
            client_id=current_app.config['RHOAUTH_OIDC_CLIENT_ID'],
            redirect_uri=secure_url_for('_auth_callback')
        )

        auth_res = request.url
        if not os.getenv('OAUTHLIB_INSECURE_TRANSPORT') and\
                'https' not in auth_res:
            auth_res = auth_res.replace('http', 'https')

        try:
            token = client.fetch_token(
                current_app.config['RHOAUTH_OIDC_TOKEN_ENDPOINT'],
                authorization_response=auth_res
            )
        except InvalidGrantError as e:
            return self.logout()

        # Validate token signatures and claims
        if self._verify_tokens(token['id_token'], token['access_token'],
                               session['nonce']):
            self._set_session_token(token['id_token'], token['access_token'],
                                    token['refresh_token'])

            for fn in self._on_login_funcs:
                fn(current_user)
            return_url = session.pop('return_url')
            session['return_url'] = return_url
            return redirect(return_url)
        else:
            return self._handle_error_response(status_code=401,
                                               message='Invalid tokens')

    def logout(self, callback_uri=None):
        """
            Handles the user logout from the session and openid provider

        :param callback_uri: full uri or path for current hostname
        :type callback_uri: str
        :return:
        """
        user = _get_user()

        if 'id_token' not in session:
            return self._logout_callback()

        id_token = session['id_token']
        logout_endpoint = current_app.config['RHOAUTH_OIDC_END_SESSION_ENDPOINT']
        logout_cb_uri = secure_url_for('_logout_callback')

        if callback_uri:
            logout_cb_uri += '?internal_redirect=' + callback_uri

        self._clear_session()
        url = '{}?id_token_hint={}&post_logout_redirect_uri={}'\
            .format(logout_endpoint, id_token, logout_cb_uri)

        for fn in self._on_logout_funcs:
            fn(user)

        return redirect(url)

    def _logout_callback(self):
        logout_redirect_uri = \
            current_app.config['RHOAUTH_OIDC_END_SESSION_REDIRECT_URI']

        if 'internal_redirect' in request.args:
            logout_redirect_uri = request.args['internal_redirect']

        return redirect(logout_redirect_uri)

    def _refresh_tokens(self, refresh_token):

        # Validate that the refresh token hasnt' expired before we request
        # new tokens. If it has expired, then perform authentication again.
        _refresh_token = jwt.JWT().unpack(refresh_token).payload()
        if not self.validate_token_claims(_refresh_token, verify_iss=False,
                                           verify_aud=False, verify_exp=True):
            g.oidc_id_token = None
            g.oidc_access_token = None
            self._clear_session()
            return

        # Token has not expired, so request new tokens
        auth = OAuth2Session(
            client_id=current_app.config['RHOAUTH_OIDC_CLIENT_ID'],
            redirect_uri=secure_url_for('_auth_callback')
        )
        try:
            token = auth.refresh_token(
                current_app.config['RHOAUTH_OIDC_TOKEN_ENDPOINT'],
                refresh_token=refresh_token,
                nonce=session['nonce'],
                client_id=current_app.config['RHOAUTH_OIDC_CLIENT_ID']
            )
        except InvalidGrantError as e:
            g.oidc_id_token = None
            g.oidc_access_token = None
            self._clear_session()
            return self._authenticate()

        # Validate token signatures and claims
        if self._verify_tokens(token['id_token'], token['access_token'],
                               session['nonce']):
            self._set_session_token(token['id_token'], token['access_token'],
                                    token['refresh_token'])

            g.oidc_id_token = jwt.JWT().unpack(token['id_token']).payload()
            g.oidc_access_token =\
                    jwt.JWT().unpack(token['access_token']).payload()

            for fn in self._on_token_refresh_funcs:
                fn(_get_user())

    def _verify_tokens(self, id_token, access_token, nonce):
        # Here we verify the token signatures
        try:
            _jws = jws.JWS()
            _id_token = _jws.verify_compact(id_token, keys=self.keys,
                                            sigalg='RS256')
            _jws.verify_compact(access_token, keys=self.keys, sigalg='RS256')
        except Exception as e:
            logger.exception(e)
            return False

        return self.validate_token_claims(_id_token, nonce=nonce)

    @classmethod
    def validate_token_claims(cls, token, verify_iss=True, verify_aud=True,
                               verify_exp=True, nonce=None):
        """
            Validates various claims from given token
        """

        if verify_iss:
            iss = current_app.config['RHOAUTH_OIDC_ISSUER']
            if token['iss'] != iss:
                logger.debug('Token issuer does not match %s != %s'
                            % (token['iss'], iss))
                return False

        if verify_aud:
            aud = current_app.config['RHOAUTH_OIDC_CLIENT_ID']
            if aud not in token['aud']:
                logger.debug('Token audience does not match. {} not in {}'
                            .format(aud, token['aud']))
                return False

        _now = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())

        if verify_exp and _now > token["exp"]:
            logger.debug('Token has expired {} > {}'
                        .format(_now, token['exp']))
            return False

        if nonce and nonce != token['nonce']:
            logger.debug('Nonce does not match %s != %s'
                        % (token['nonce'], nonce))
            return False

        return True

    def _handle_error_response(self, status_code, message=None):
        if self._error_view:
            return self._error_view(status_code, message)
        return abort(status_code, message)

    def error_view(self, view_fn):
        self._error_view = view_fn
        return view_fn

    def on_refresh_token(self, view_fn):
        """
        Callable to be executed after a user's token has successfully
        refreshed

        oidc = OpenIDConnect()
        @oidc.on_refresh_token
        def sync_user_data(user)
            pass

        :param view_fn:
        :type view_fn: callable(RHOAUTH_OIDC_USER_CLASS)
        :return:
        """
        self._on_token_refresh_funcs.append(view_fn)

    def on_logout(self, view_fn):
        """
        Callable to be executed after a user has logged out

        Example:

        oidc = OpenIDConnect()
        @oidc.on_logout
        def remove_from_live_users(user)
            user.is_live = False
            db.session.add(user)
            db.session.commit()

        :param view_fn:
        :type view_fn: callable(RHOAUTH_OIDC_USER_CLASS)
        :return:
        """
        self._on_logout_funcs.append(view_fn)

    def on_login(self, view_fn):
        """
        Callable to be executed after a user has logged in

        oidc = OpenIDConnect()
        @oidc.on_login
        def add_to_live_users(user)
            user.is_live = True
            db.session.add(user)
            db.session.commit()

        :param view_fn:
        :type view_fn: callable(RHOAUTH_OIDC_USER_CLASS)
        :return:
        """
        self._on_login_funcs.append(view_fn)


class BaseOpenIDUser(object):
    if not PY2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        __hash__ = object.__hash__

    def __init__(self, id_token, access_token):
        self.id_token = id_token
        self.access_token = access_token

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def full_name(self):
        return None

    @property
    def roles(self):
        return None

    def get_id(self):
        return None

    def has_role(self, role):
        return False


class OpenIDUser(BaseOpenIDUser):

    @property
    def is_active(self):
        return self.id_token or self.access_token

    @property
    def is_authenticated(self):
        if self.id_token:
            return OpenIDConnect.validate_token_claims(
                self.id_token, verify_iss=True, verify_aud=True, verify_exp=True
            )
        elif self.access_token:
            return OpenIDConnect.validate_token_claims(
                self.access_token, verify_iss=True, verify_aud=True, verify_exp=True
            )
        return False

    @property
    def is_anonymous(self):
        return self.id_token is None and self.access_token

    @property
    def full_name(self):
        return self.get_property('name')

    @property
    def email(self):
        return self.get_property('email')

    @property
    def roles(self):
        if self.access_token and 'resource_access' in self.access_token:
            client_id = current_app.config['RHOAUTH_OIDC_CLIENT_ID']
            if client_id in self.access_token['resource_access'] and \
                'roles' in self.access_token['resource_access'][client_id]:
                return self.access_token['resource_access'][client_id]['roles']
        return []

    def get_id(self):
        return self.get_property('sub')

    def has_role(self, role):
        roles = self.roles
        return len(roles) > 0 and role in roles

    def get_property(self, property):
        """
        search id_token, then access_token for a given property
        :param property: property to access
        :type property: str
        :return:
        :rtype any
        """
        if self.id_token and property in self.id_token:
            return self.id_token[property]
        elif self.access_token and property in self.access_token:
            return self.access_token[property]

        return None


class AnonymousOpenIDUser(BaseOpenIDUser):
    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    @property
    def full_name(self):
        return 'Anonymous User'

    @property
    def email(self):
        return None

    @property
    def roles(self):
        return None

    @property
    def id(self):
        return self.get_id()

    def get_id(self):
        return None

    def has_role(self, role):
        return False


def _get_user():
    # Create a user for local proxy
    user_cls = current_app.config['RHOAUTH_OIDC_USER_CLASS']
    id_token = session.get('id_token')  # type: str
    access_token = session.get('access_token')  # type: str

    # If access token is none, then check if we have it as part of an api
    # request instead
    if access_token is None:
        oid = current_app.extensions[OpenIDConnect.EXTENSION_NAME]
        access_token = get_access_token_from_request(oid.keys)

    if id_token is None and access_token is None:
        return AnonymousOpenIDUser(id_token, access_token)

    _jwt = jwt.JWT()
    _id_token = None  # type: dict[str, any] or None
    _access_token = None  # type: dict[str, any] or None

    if id_token:
        _id_token = _jwt.unpack(id_token).payload()

    if access_token:
        _access_token = _jwt.unpack(access_token).payload()

    # This logic allows the user to log in with either an id_token,
    # access_token, or both. This is useful when programmatically
    # logging into accounts via
    # requests_oauthlib's OAuth2Session & LegacyApplicationClient
    _token = _id_token
    if not _id_token:
        _token = _access_token

    if not OpenIDConnect.validate_token_claims(_token, verify_aud=False):
        return AnonymousOpenIDUser(_id_token, _access_token)

    return user_cls(_id_token, _access_token)


def _user_context_processor():
    return dict(current_user=_get_user())
