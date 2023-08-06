import logging

import click
from click import ClickException
from simple_rest_client.api import API
from simple_rest_client.resource import Resource

from vgscli._version import __version__
from vgscli.errors import VaultNotFoundError

logger = logging.getLogger(__name__)

env_url = {
    'dev': 'https://audits.verygoodsecurity.io',
    'prod': 'https://audits.apps.verygood.systems',
}


class AccessLogsResource(Resource):
    actions = {
        'retrieve': {'method': 'GET', 'url': 'access-logs/{}'},
        'list': {'method': 'GET', 'url': 'access-logs'},
    }


def create_api(ctx, vault_id, environment, token):
    api = API(
        api_root_url=env_url[environment],
        params={},  # default params
        headers={
            'VGS-Tenant': vault_id,
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'User-Agent': 'VGS CLI {}'.format(__version__),
            'Authorization': 'Bearer {}'.format(token)
        },  # default headers
        timeout=50,  # default timeout in seconds
        append_slash=False,  # append slash to final url
        json_encode_body=True,  # encode body as json
    )
    api.add_resource(resource_name='access_logs', resource_class=AccessLogsResource)
    return api


def get_api_url(ctx, vault_id, api):
    response = api.accounts_api.get_vault_by_id(vault_id)
    try:
        return response.body['data'][0]['links']['vault_management_api']
    except (KeyError, IndexError):
        # if we weren't able to extract the vault_management_api it means that the provided vault_id doesn't exist
        raise VaultNotFoundError(vault_id, ctx)
