# pylint: disable=too-many-locals

'''
Entry point for cli utility
'''

import click
import jwt
import pkg_resources
import requests
import yaml
from matatika.config import MatatikaConfig
from matatika.dataset import Dataset
from matatika.exceptions import ContextNotSetError
from matatika.exceptions import DatasetNotFoundError
from matatika.exceptions import MatatikaException
from matatika.exceptions import WorkspaceNotFoundError
from matatika.library import MatatikaClient

version = pkg_resources.require("matatika")[0].version


class ExceptionHandler(click.Group):
    '''CLI entrypoint and error handling'''

    def invoke(self, ctx):
        '''Invoke method override'''

        try:
            return super().invoke(ctx)

        except ContextNotSetError as err:
            click.secho(str(err), fg='red')

        except jwt.exceptions.DecodeError as err:
            click.secho(str(err), fg='red')
            click.secho(
                """Please check your authentication token is correct and valid""", fg='red')

        except requests.exceptions.HTTPError as err:
            click.secho(str(err), fg='red')
            click.secho("""Please check your authentication token has not expired and the correct
                endpoint is specified""", fg='red')

        except WorkspaceNotFoundError as err:
            click.secho(str(err), fg='red')

        except DatasetNotFoundError as err:
            click.secho(str(err), fg='red')

        except MatatikaException as err:
            click.secho(str(err), fg='red')


@click.group(cls=ExceptionHandler)
@click.pass_context
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--endpoint-url", "-e", help="Endpoint URL")
@click.version_option(version=version)
def matatika(ctx, auth_token, endpoint_url):
    '''CLI entrypoint and base command'''

    ctx.ensure_object(dict)
    ctx.obj['auth_token'] = auth_token
    ctx.obj['endpoint_url'] = endpoint_url


@matatika.command('publish', short_help='Publish one or more dataset(s)')
@click.pass_context
@click.argument('dataset-file', type=click.Path(exists=True))
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
def publish(ctx, dataset_file, workspace_id):
    """Publish one or more dataset(s) from a YAML file into a workspace"""

    config = MatatikaConfig()
    credentials = _resolve_credentials(ctx, config)
    credentials[2] = (
        workspace_id if workspace_id else config.get_default_workspace())
    client = MatatikaClient(*credentials)

    with open(dataset_file, 'r') as datasets_file:
        datasets = yaml.safe_load(datasets_file)['datasets']

    for alias in datasets:
        datasets[alias]['alias'] = alias

    publish_responses = client.publish(datasets)

    click.secho(f"Successfully published {len(publish_responses)} dataset(s)\n",
                fg='green')

    ids = ['DATASET ID']
    aliases = ['ALIAS']
    titles = ['TITLE']
    statuses = ['STATUS']

    for response in publish_responses:
        dataset = Dataset.from_dict(response.json())

        if response.status_code == 200:
            status = click.style("UPDATED", fg='cyan')
        elif response.status_code == 201:
            status = click.style("NEW", fg='magenta')
        else:
            status = click.style("UNKNOWN", fg='red')

        ids.append(dataset.dataset_id)
        aliases.append(dataset.alias)
        titles.append(dataset.title)
        statuses.append(status)

    _table(ids, aliases, titles, statuses)


@matatika.group('list', short_help='List all available resources')
def list_():
    """Display a list of all available resources of a specified type"""


@list_.command('workspaces', short_help='List all available workspaces')
@click.pass_context
def list_workspaces(ctx):
    """Display a list of all available workspaces"""

    client = MatatikaClient(*_resolve_credentials(ctx, MatatikaConfig()))
    workspaces = client.list_resources('workspaces')

    ids = ['WORKSPACE ID']
    names = ['NAME']

    for workspace in workspaces:
        ids.append(workspace['id'])
        names.append(workspace['name'])

    _table(ids, names)
    click.echo(f"\nTotal workspaces: {len(workspaces)}")


@list_.command('datasets', short_help='List all available datasets')
@click.pass_context
@click.option('--workspace-id', '-w', type=click.UUID, help='Workspace ID')
def list_datasets(ctx, workspace_id):
    """Display a list of all available datasets"""

    config = MatatikaConfig()
    credentials = _resolve_credentials(ctx, config)
    credentials[2] = (
        workspace_id if workspace_id else config.get_default_workspace())
    client = MatatikaClient(*credentials)
    datasets = client.list_resources('datasets')

    ids = ['DATASET ID']
    aliases = ['ALIAS']
    titles = ['TITLE']

    for dataset in datasets:
        ids.append(dataset['id'])
        aliases.append(dataset['alias'])
        titles.append(dataset['title'])

    _table(ids, aliases, titles)
    click.echo(f"\nTotal datasets: {len(datasets)}")


@matatika.command('use', short_help='View or set the default workspace')
@click.pass_context
@click.option('--workspace-id', '-w', type=click.UUID, help='Workspace ID')
def use(ctx, workspace_id):
    """View or set the workspace context used by other commands"""

    config = MatatikaConfig()

    if workspace_id:
        client = MatatikaClient(*_resolve_credentials(ctx, config))
        workspaces = client.list_resources('workspaces')

        workspace_id = str(workspace_id)
        workspace_ids = [workspaces[i]['id']
                         for i in range(len(workspaces))]

        if workspace_id not in workspace_ids:
            raise WorkspaceNotFoundError(
                config.get_endpoint_url(), workspace_id)

        config.set_default_workspace(workspace_id)

    workspace_context = config.get_default_workspace()
    click.secho(
        f"Workspace context set to {workspace_context}", fg='green')


@matatika.command('login', short_help='Login to a Matatika account')
@click.option('--auth-token', '-a', required=True, help='Authentication token')
@click.option('--endpoint-url', '-e', default='https://catalog.matatika.com/api',
              help='Endpoint URL')
def login(auth_token, endpoint_url):
    """Login to a Matatika account and set the authentication context used by other commands"""

    client = MatatikaClient(auth_token, endpoint_url, None)
    profile = client.profile()

    config = MatatikaConfig()
    config.set_auth_token(auth_token)
    config.set_endpoint_url(endpoint_url)

    click.secho("Successfully logged in\n", fg='green')
    _table(['ID', 'NAME'], [profile['id'],
                            profile['name']], fg_colour='green')


@matatika.command("fetch", short_help="Fetch the data from a dataset")
@click.pass_context
@click.argument("dataset-id", type=click.UUID)
@click.option("--output-file", "-f", type=click.Path(writable=True), help="Output file path")
def fetch(ctx, dataset_id, output_file):
    """Fetch the data from a dataset"""

    client = MatatikaClient(*_resolve_credentials(ctx, MatatikaConfig()))
    data = client.fetch(dataset_id, raw=True)

    if output_file:
        with open(output_file, "w") as file_:
            file_.write(data)
        click.secho(f"Dataset {dataset_id} data successfully written to {output_file}",
                    fg='green')

    else:
        click.secho(f"*** START DATASET {dataset_id} DATA CHUNK STDOUT DUMP ***",
                    err=True,  fg='yellow')
        click.echo(data)
        click.secho(f"*** END DATASET {dataset_id} DATA CHUNK STDOUT DUMP ***",
                    err=True,  fg='yellow')


def _table(*cols, spacing=4, fg_colour='reset'):
    for col in cols:
        for i, cell in enumerate(col):
            col[i] = cell.ljust(len(max(col, key=len)))

    for i, _ in enumerate(cols[0]):
        click.secho(
            (' ' * spacing).join([col[i] for col in cols]), fg=fg_colour)


def _resolve_credentials(ctx, config):

    auth_token = (
        ctx.obj['auth_token'] if ctx.obj['auth_token'] else config.get_auth_token())

    endpoint_url = (
        ctx.obj['endpoint_url'] if ctx.obj['endpoint_url'] else config.get_endpoint_url())

    return [auth_token, endpoint_url, None]
