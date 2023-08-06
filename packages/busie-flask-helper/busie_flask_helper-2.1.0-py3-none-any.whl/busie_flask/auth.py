"""Authentication Lib"""
import json
from functools import wraps
from six.moves.urllib.request import urlopen

import rsa
from jose import jwt
from flask import request, jsonify, _request_ctx_stack


class AuthError(Exception):
    """
    For handling Auth related Errors
    :param error: dict, the auth related error
    :param status_code: int, the status code to return with the response
    """
    def __init__(self, error: dict, status_code: int) -> None:
        self.error = error
        self.status_code = status_code


class AuthHelper:
    """Methods for signing, verifying, and decoding tokens"""
    def __init__(self, app=None):
        self.__algorithms = None
        self.__auth0_domain = None
        self.__audience = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize a Flask application, setting the __secret property and adding self to
        app extensions

        :param app: A Flask application
        """

        self.__algorithms = app.config.get('AUTH0_ALGORITHMS')
        self.__audience = app.config.get('AUTH0_AUDIENCE')
        self.__auth0_domain = app.config.get('AUTH0_DOMAIN')
        if not (self.__algorithms and self.__audience and self.__auth0_domain):
            raise RuntimeError('AUTH0_ALGORITHMS, AUTH0_AUDIENCE, and AUTH0_DOMAIN must be in application config.')

        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        app.extensions['auth'] = self

        @app.errorhandler(AuthError)
        def handle_auth_header(ex):  # pylint: disable=unused-variable
            response = jsonify(ex.error)
            response.status_code = ex.status_code
            return response

    def requires_auth(self, f):
        """Determines if the Access Token is valid"""
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                token = self.get_token_auth_header()
                rsa_key = self.get_rsa_key_from_unverified_token(token)
                if rsa_key:
                    payload = self.handle_rsa_decode(rsa_key, token)
                    _request_ctx_stack.top.current_user = payload
                    return f(*args, **kwargs)
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to find appropriate key'
                }, 401)
            except AuthError as ex:
                raise AuthError(ex.error, ex.status_code) from ex
            except Exception as ex:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse auth token'
                }, 401) from ex

        return decorated

    def get_rsa_key_from_unverified_token(self, token: str) -> dict:
        """
        Use the provided token to find a matching rsa key from the auth0 domain
        :param token: str, the token that should have a matching rsa key
        :return: dict, None. The resulting rsa key if it exists else none

        NOTE: returns None when no key is found.
        """
        try:
            jsonurl = urlopen(f'https://{self.__auth0_domain}/.well-known/jwks.json')
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            for key in jwks['keys']:

                if key['kid'] == unverified_header.get('kid', None):
                    return {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }

            return None  # an rsa key matching the desired kid was not found -> return None

        except jwt.JWTError as ex:
            raise AuthError({
                'code': 'invalid_error',
                'description': 'Unable to decode the provided auth token'
            }, 401) from ex

    def handle_rsa_decode(self, rsa_key: dict, token: str) -> dict:
        """
        Decode the auth token using the provided rsa key
        :return: dict -> the decoded payload
        :raise: AuthError
        """
        try:
            if rsa_key.get('alg') != 'RS256' and rsa_key.get('use') != 'sig':
                raise AuthError({
                    'code': 'token_invalid',
                    'description': 'Can only decode RSA auth tokens at this time.'
                }, 401)

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=self.__algorithms,
                audience=self.__audience,
                issuer=f'https://{self.__auth0_domain}/'
            )

        except jwt.ExpiredSignatureError as ex:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Auth token is expired'
            }, 401) from ex

        except jwt.JWTClaimsError as ex:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Invalid claims, please check audience claim'
            }, 401) from ex

        return payload

    def requires_scope(self, required_scope: str) -> bool:
        """
        Determine if the required scope is present in the access token
        :param required_scope: str, the scope required to access the resource
        """
        token = self.get_token_auth_header()
        unverified_claims = jwt.get_unverified_claims(token)

        if unverified_claims.get('scope', None):
            token_scopes = unverified_claims['scope'].split()

            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True

        return False

    def requires_permission(self, required_permission: str) -> bool:
        """
        Determine if the required permission is present in the access token permissions
        :param required_permission: str, the scope required to access the resource
        """
        token = self.get_token_auth_header()
        unverified_claims = jwt.get_unverified_claims(token)

        if unverified_claims.get('permissions', None):
            token_permissions = unverified_claims['permissions']

            for token_permission in token_permissions:
                if token_permission == required_permission:
                    return True

        return False

    @staticmethod
    def get_token_auth_header() -> str:
        """Obtains the Access Token from the request context Authorization Header"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'An Authorization Header is required to access this resource'
            }, 401)

        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must have format `Bearer <token>`'
            }, 401)

        token = parts[1]
        return token
