"""Test Authentication Lib"""
import pytest
from busie_flask.auth import AuthHelper, AuthError

@pytest.fixture
def mock_app(mocker):
    app = mocker.MagicMock()
    app.config.get.return_value = 'secret'
    return app

def test_auth_error(mocker):
    """
    - Sets error, status_code to the provided values
    """
    mock_error = {'foo': 'bar'}
    mock_status_code = 401
    a = AuthError(mock_error, mock_status_code)
    assert isinstance(a, Exception)
    assert a.error == mock_error
    assert a.status_code == mock_status_code

    with pytest.raises(AuthError):
        raise AuthError(mock_error, mock_status_code)

def test_authentication_helper_init(mocker):
    """
    - Sets _secret to None
    - Calls self.init_app with app if app provided
    """
    mock_init_app = mocker.patch('busie_flask.auth.AuthHelper.init_app')

    res = AuthHelper()
    mock_init_app.assert_not_called()
    assert hasattr(res, '_AuthHelper__algorithms')
    assert getattr(res, '_AuthHelper__algorithms') is None
    assert hasattr(res, '_AuthHelper__auth0_domain')
    assert getattr(res, '_AuthHelper__auth0_domain') is None
    assert hasattr(res, '_AuthHelper__audience')
    assert getattr(res, '_AuthHelper__audience') is None

    res = AuthHelper(app='foo')
    mock_init_app.assert_called_once_with('foo')


def test_init_app(mock_app, mocker):
    """
    - Throws RuntimeError if app.config does not have AUTH_SECRET
    - Adds self to app.extensions as `auth`
    """
    del mock_app.extensions

    auth = AuthHelper()
    auth.init_app(mock_app)
    mock_app.config.get.assert_has_calls([
        mocker.call('AUTH0_ALGORITHMS'),
        mocker.call('AUTH0_AUDIENCE'),
        mocker.call('AUTH0_DOMAIN')
    ])
    assert mock_app.extensions
    assert mock_app.extensions.get('auth') == auth

    mock_app.config.get.return_value = None
    with pytest.raises(RuntimeError):
        auth.init_app(mock_app)

def test_get_token_auth_header(mocker):
    """
    - raise AuthError if `Authorization` not in request headers
    - raise AuthError if auth header does not have correct format
    - returns the token from the auth header
    """
    mock_request = mocker.patch('busie_flask.auth.request')
    valid_header = 'Bearer sometokenheredoesntmatter'
    invalid_headers = [
        None,
        'a token',
        'bearer',
        'some token with too many parts'
    ]
    auth = AuthHelper()
    for header in invalid_headers:
        mock_request.headers.get.return_value = header
        with pytest.raises(AuthError):
            auth.get_token_auth_header()
    mock_request.headers.get.return_value = valid_header
    token = auth.get_token_auth_header()
    assert isinstance(token, str)
    assert token == valid_header.split()[1]

def test_get_rsa_key_from_unverified_token(mocker):
    """
    - Raise AuthError if the provided token cannot be decoded as a jwt
    - Return an object representation of an RSA key if a match is found
    - Return None if a match is not found
    """
    mock_url_open = mocker.patch('busie_flask.auth.urlopen')
    mock_json = mocker.patch('busie_flask.auth.json')
    mock_jwt = mocker.patch('busie_flask.auth.jwt')
    mock_jwt.DecodeError = Exception
    mock_domain = 'foobar.com'
    mock_token = 'sometokendoesntmatteraslongasitsastring'
    mock_jwk = {'kid': 'someKID', 'kty': 'someKTY', 'use': 'someUSE', 'n': 'n', 'e': 'e'}
    mock_json.loads.return_value = {
        'keys': [mock_jwk]
    }
    mock_jwt.get_unverified_header.return_value = {'kid': mock_jwk['kid']}

    auth = AuthHelper()
    auth._AuthHelper__auth0_domain = mock_domain
    rsa_key = auth.get_rsa_key_from_unverified_token(mock_token)
    
    mock_url_open.assert_called_once_with(
        f'https://{mock_domain}/.well-known/jwks.json'
    )
    mock_json.loads.assert_called_once_with(mock_url_open.return_value.read.return_value)
    mock_jwt.get_unverified_header.assert_called_once_with(mock_token)
    assert rsa_key is not None
    assert 'kty' in rsa_key and rsa_key['kty'] == mock_jwk['kty']
    assert 'kid' in rsa_key and rsa_key['kid'] == mock_jwk['kid']
    assert 'use' in rsa_key and rsa_key['use'] == mock_jwk['use']
    assert 'n' in rsa_key and rsa_key['n'] == mock_jwk['n']
    assert 'e' in rsa_key and rsa_key['e'] == mock_jwk['e']

    mock_jwt.get_unverified_header.return_value = {'kid': 'invalid'}
    assert auth.get_rsa_key_from_unverified_token(mock_token) is None

    mock_jwt.get_unverified_header.side_effect = mock_jwt.DecodeError
    with pytest.raises(AuthError):
        auth.get_rsa_key_from_unverified_token(mock_token)

def test_handle_rsa_decode(mocker):
    """
    - Raise AuthError on token expired
    - Raise AuthError on InvalidAudience
    - Raise AuthError on invalid issuer
    - return the decoded token object
    """
    mock_jwt = mocker.patch('busie_flask.auth.jwt')
    mock_rsa = mocker.patch('busie_flask.auth.rsa')
    class MockExpiredSignature(Exception):
        """Mock Expired Signature Error"""
    class MockInvalidAudience(Exception):
        """Mock Invalid Audience Error"""
    class MockInvalidIssuer(Exception):
        """Mock Invalid Issuer Errror"""
    mock_token = 'sometoken'
    mock_key = {'alg': 'RS256', 'use': 'sig', 'n': 'thenvalue', 'e': 'theevalue'}
    mock_algorithms = ['algos']
    mock_domain = 'foo.com'
    mock_audience = 'someaudience'
    auth = AuthHelper()
    auth._AuthHelper__auth0_domain = mock_domain
    auth._AuthHelper__algorithms = mock_algorithms
    auth._AuthHelper__audience = mock_audience

    decoded = auth.handle_rsa_decode(mock_key, mock_token)
    mock_rsa.PublicKey.assert_called_once_with(mock_key['n'], mock_key['e'])
    mock_rsa.PublicKey.return_value.save_pkcs1.assert_called_once()
    mock_jwt.decode.assert_called_once_with(
        mock_token,
        mock_rsa.PublicKey.return_value.save_pkcs1.return_value,
        algorithms=mock_algorithms,
        audience=mock_audience,
        issuer=f'https://{mock_domain}/'
    )
    assert decoded == mock_jwt.decode.return_value

    mock_jwt.ExpiredSignatureError = MockExpiredSignature
    mock_jwt.InvalidAudienceError = MockInvalidAudience
    mock_jwt.InvalidIssuerError = MockInvalidIssuer
    exceptions = [mock_jwt.ExpiredSignatureError, mock_jwt.InvalidAudienceError, mock_jwt.InvalidIssuerError, AuthError]
    for e in exceptions:
        mock_jwt.decode.side_effect = e
        args_list = [
            mock_key if e is not AuthError else {},
            'token'
        ]
        with pytest.raises(AuthError):
            auth.handle_rsa_decode(*args_list)

def test_requires_auth(mocker):
    """
    - Raise an auth error if AuthError is caught
    - Raise an auth error if base Exception is caught
    - Raise an auth error if get rsa key returns None
    - invokes the decorated function after setting request context current user
    """
    was_called = mocker.MagicMock()
    mock_get_auth_header = mocker.patch('busie_flask.auth.AuthHelper.get_token_auth_header')
    mock_get_rsa_key = mocker.patch('busie_flask.auth.AuthHelper.get_rsa_key_from_unverified_token')
    mock_handle_decode = mocker.patch('busie_flask.auth.AuthHelper.handle_rsa_decode')
    mock_context = mocker.patch('busie_flask.auth._request_ctx_stack')
    auth = AuthHelper()

    @auth.requires_auth
    def foo(*args, **kwargs):
        return was_called(*args, **kwargs)

    res = foo('something', **{'something': 'else'})
    was_called.assert_called_once_with('something', **{'something': 'else'})
    assert res == was_called.return_value
    mock_get_auth_header.assert_called_once()
    mock_get_rsa_key.assert_called_once_with(mock_get_auth_header.return_value)
    mock_handle_decode.assert_called_once_with(mock_get_rsa_key.return_value, mock_get_auth_header.return_value)
    assert mock_context.top.current_user == mock_handle_decode.return_value

    mock_get_rsa_key.return_value = None
    with pytest.raises(AuthError):
        foo()

    mock_get_auth_header.side_effect = AuthError
    with pytest.raises(AuthError):
        foo()

    mock_get_auth_header.side_effect = Exception
    with pytest.raises(AuthError):
        foo()

def test_requires_scope(mocker):
    """
    - Return True if the required scope is in the token scopes
    - Return False otherwise
    """

    mock_token = 'sometoken'
    mock_get_token = mocker.patch('busie_flask.auth.AuthHelper.get_token_auth_header')
    mock_get_token.return_value = mock_token
    mock_jwt = mocker.patch('busie_flask.auth.jwt')
    mock_jwt.decode.return_value = {'scope': 'foo bar foobar'}

    auth = AuthHelper()
    assert auth.requires_scope('foo')
    mock_get_token.assert_called_once()
    mock_jwt.decode.assert_called_once_with(mock_token, verify=False)

    assert not auth.requires_scope('somethingnotthere')
    mock_jwt.decode.return_value = {}
    assert not auth.requires_scope('foo')
