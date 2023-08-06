import os

from simple_rest_client.exceptions import ClientError

from vgscli.auth_server import AuthServer
from vgscli.errors import AuthenticationError, AuthenticationRequiredError, TokenNotValidError, \
    AutoAuthenticationError
from vgscli.keyring_token_util import KeyringTokenUtil

token_util = KeyringTokenUtil()
TOKEN_FILE_NAME = 'vgs_token'

CLIENT_ID = os.environ.get('VGS_CLIENT_ID')
CLIENT_SECRET = os.environ.get('VGS_CLIENT_SECRET')

AUTO_LOGIN = CLIENT_ID and CLIENT_SECRET


def handshake(ctx, environment):
    try:
        token_util.validate_refresh_token()
        if not token_util.validate_access_token():
            AuthServer(environment).refresh_authentication()
    except TokenNotValidError:
        raise AuthenticationRequiredError(ctx)
    except Exception as e:
        raise AuthenticationError(ctx, e.args[0])


def login(ctx, environment):
    try:
        return AuthServer(environment).login(environment)
    except Exception as e:
        raise AuthenticationError(ctx, e.args[0])


def logout(ctx, environment):
    try:
        AuthServer(environment).logout()
        token_util.clear_tokens()
        token_util.remove_encryption_secret()
    except Exception as e:
        raise AuthenticationError(ctx, e.args[0])


def auto_login(ctx, environment):
    if not AUTO_LOGIN:
        return False

    if not token_util.is_access_token_valid():
        try:
            AuthServer(environment).auto_login(CLIENT_ID, CLIENT_SECRET)
        except ClientError:
            raise AutoAuthenticationError(ctx)

    return True
