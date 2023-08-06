#!/usr/bin/env python
import urllib
import threading
import time
import urllib.parse
import webbrowser

import click

from vgscli import auth_api
from vgscli.auth_utils import code_challenge, generate_code_verifier
from vgscli.utils import is_port_accessible
from vgscli.keyring_token_util import KeyringTokenUtil
from vgscli.callback_server import RequestServer
from vgscli.token_handler import CodeHandler


class AuthServer:
    env_url = {
        'dev': 'https://auth.verygoodsecurity.io',
        'prod': 'https://auth.verygoodsecurity.com'
    }
    token_util = KeyringTokenUtil()
    token_handler = CodeHandler()

    # Api
    CLIENT_ID = 'vgs-cli-public'
    SCOPE = 'openid'
    AUTH_URL = '{base_url}/auth/realms/vgs/protocol/openid-connect/auth'
    CALLBACK_SUFIX = '/callback'

    # AuthZ
    code_verifier = generate_code_verifier()
    code_method = 'S256'
    oauth_access_token = None

    # Server constants.
    # Ports have been chosen based on Unassigned port list: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=111
    ports = [7745, 8390, 9056]
    host = '0.0.0.0'
    accessible_port = None
    app = None

    def __init__(self, environment):
        self.accessible_port = next(port for port in self.ports if is_port_accessible(self.host, port))
        self.app = RequestServer(self.host, self.accessible_port)
        self.environment = environment
        self.auth_api = auth_api.create_api(environment)

    def login(self, environment):
        thread = self.ServerThread(self.app)
        thread.daemon = True
        thread.start()

        url = self.AUTH_URL.format(
            base_url=self.env_url[environment]
        ) + ('?response_type=code&redirect_uri={host}/callback'
             '&client_id={client_id}'
             '&scope={scope}'
             '&code_challenge={code_challenge}'
             '&code_challenge_method={code_challenge_method}').format(
            host=urllib.parse.quote(self.__get_host()),
            client_id=urllib.parse.quote(self.CLIENT_ID),
            scope=urllib.parse.quote(self.SCOPE),
            code_challenge=code_challenge(self.code_verifier),
            code_challenge_method=self.code_method
        )
        if not webbrowser.open(url, new=1, autoraise=True):
            click.echo(f'Can not open your browser, please open this URL in your browser: {url}')

        while self.token_handler.get_code() is None:
            time.sleep(1)
        self.retrieve_access_token()
        return self.token_util.get_access_token()

    def logout(self):
        auth_api.logout(self.auth_api, self.CLIENT_ID, self.token_util.get_access_token(), self.token_util.get_refresh_token())

    def refresh_authentication(self):
        self.token_util.put_tokens(auth_api.refresh_token(self.auth_api).body)

    def retrieve_access_token(self):
        callback_url = self.__get_host() + self.CALLBACK_SUFIX
        response = auth_api.get_token(self.auth_api, self.token_handler.get_code(), self.code_verifier, callback_url)
        self.set_access_token(response.body)

    def set_access_token(self, token):
        self.token_util.put_tokens(token)

    def __get_host(self):
        return 'http://' + self.host + ':' + str(self.accessible_port)

    def auto_login(self, client_id, secret):
        response = auth_api.get_auto_token(self.auth_api, client_id=client_id, client_secret=secret)
        self.set_access_token(response.body)

    class ServerThread(threading.Thread):

        def __init__(self, app):
            self.app = app
            threading.Thread.__init__(self)

        def run(self):
            self.app.run()
