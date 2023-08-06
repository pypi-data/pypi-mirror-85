import click

from pkg_resources import iter_entry_points
from click_plugins import with_plugins

from vgscli import auth
from vgscli.access_logs import prepare_filter, fetch_logs, format_logs, wrap_records
from vgscli.click_extensions import Config, DateTimeDuration
from vgscli.vaults_api import create_api as create_vaults_api
from vgscli.audits_api import create_api as create_audits_api
from vgscli.auth import auto_login, handshake, token_util
from vgscli.errors import handle_errors
from vgscli.routes import dump_all_routes, sync_all_routes
from vgscli.utils import resolve_env


@with_plugins(iter_entry_points('vgs.plugins'))
@click.group()
@click.option("--debug", "-d", is_flag=True, help="Enables debug mode.", default=False)
@click.option("--environment", "-e", help="VGS environment.", hidden=True)
@click.version_option(message='%(version)s')
@click.pass_context
def cli(ctx, debug, environment):
    """
    Command Line Tool for programmatic configurations on VGS.
    """
    ctx.debug = debug

    env = resolve_env(environment)
    ctx.obj = Config(debug, env)

    auto_login(ctx, env)


@with_plugins(iter_entry_points('vgs.get.plugins'))
@cli.group()
def get():
    """
    Get VGS resource.
    """
    pass


@with_plugins(iter_entry_points('vgs.apply.plugins'))
@cli.group()
def apply():
    """
    Create or update VGS resource.
    """
    pass


@with_plugins(iter_entry_points('vgs.logs.plugins'))
@cli.group()
def logs():
    """
    Prints VGS logs.

    \b\bExamples:

    # Return all logs available for a vault\t\t\t\t\t\t
    vgs logs access -V tntbnqdfizv

    # Show all logs in the last hour\t\t\t\t\t\t
    vgs logs access -V tntbnqdfizv --since=1h

    # Show all logs after a specific date\t\t\t\t\t\t
    vgs logs access -V tntbnqdfizv --since=2020-08-18T11:40:45

    # Display only the most recent 25 log records\t\t\t\t\t\t
    vgs logs access -V tntbnqdfizv --tail=25
    """
    pass


def validate_tail(ctx, param, value):
    try:
        if value > 0:
            return value
        elif value != -1:
            raise ValueError
    except ValueError:
        raise click.BadParameter('need to be positive value, larger than 0')


@logs.command('access')
@click.option('--output', '-o', help='Output format', type=click.Choice(['json', 'yaml']), default='yaml',
              show_default=True)
# @click.option('--follow', '-f', help='Specify to stream logs as they appear on the VGS dashboard.', is_flag=True, default=False)
@click.option('--since',
              help='Only show logs newer than a relative duration like 30s, 5m, or 3h or after a specific RFC 3339 date.',
              type=DateTimeDuration(formats=["%Y-%m-%dT%H:%M:%S"]))
@click.option('--tail', help='Number of log records to show. Defaults to all logs if unspecified.', default=-1,
              callback=validate_tail)
@click.option('--until',
              help='Only show logs older than a relative duration like 30s, 5m, or 3h or before a specific RFC 3339 date.',
              type=DateTimeDuration(formats=["%Y-%m-%dT%H:%M:%S"]))
@click.option('--vault', '-V', help="Vault ID", required=True)
@click.pass_context
def access(ctx, vault, **kwargs):
    """
    Get access logs
    """
    handshake(ctx, ctx.obj.env)

    audits_api = create_audits_api(ctx, vault, ctx.obj.env, token_util.get_access_token())

    filters = prepare_filter({
        'tenant_id': vault,
        'from': kwargs.get('since'),
        'to': kwargs.get('until'),
    })

    for res in fetch_logs(audits_api, filters, kwargs.get('tail')):
        click.echo(format_logs(wrap_records(res), kwargs.get('output')))

    # while kwargs['follow']:
    #     res = fetch_logs(audits_api, filters, kwargs.get('tail'))
    #     click.echo(format_logs(res, kwargs.get('output')))
    #     time.sleep(3)


@get.command('routes')
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.pass_context
@handle_errors
def get_routes(ctx, vault):
    """
    Get routes
    """
    handshake(ctx, ctx.obj.env)

    routes_api = create_vaults_api(ctx, vault, ctx.obj.env, token_util.get_access_token())
    dump = dump_all_routes(routes_api)
    click.echo(dump)


@apply.command('routes')
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.option("--filename", "-f", help="Filename for the input data", type=click.File('r'), required=True)
@click.pass_context
@handle_errors
def apply_routes(ctx, vault, filename):
    """
    Create or update VGS routes.
    """
    handshake(ctx, ctx.obj.env)

    route_data = filename.read()
    vault_management_api = create_vaults_api(ctx, vault, ctx.obj.env, token_util.get_access_token())
    sync_all_routes(vault_management_api, route_data,
                    lambda route_id: click.echo(f'Route {route_id} processed'))
    click.echo(f'Routes updated successfully for vault {vault}')


@cli.command()
@click.pass_context
def login(ctx):
    """
    Login to VGS via browser.
    """
    auth.login(ctx, ctx.obj.env)


@cli.command()
@click.pass_context
def logout(ctx):
    """
    Logout from VGS.
    """
    auth.logout(ctx, ctx.obj.env)


if __name__ == "__main__":
    cli()
