import click

from sym.cli.helpers.ec2.factory import get_ec2_client

from ..decorators import loses_interactivity, require_bins, require_login
from ..helpers.global_options import GlobalOptions
from ..helpers.options import resource_argument
from ..helpers.ssh import start_tunnel
from .sym import sym


@sym.command(hidden=True, short_help="Starts a SSH session over SSM")
@resource_argument
@click.option("--instance", help="Instance ID to connect to", required=True)
@click.option("--port", default=22, type=int, show_default=True)
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("aws", "session-manager-plugin")
@require_login
def ssh_session(options: GlobalOptions, resource: str, instance: str, port: int):
    """Use approved creds for RESOURCE to tunnel a SSH session through an SSM session."""
    client = options.create_saml_client(resource)
    running_instance = get_ec2_client(client).load_instance_by_alias(instance)
    new_client = client.clone(
        options=client.options.clone(aws_region=running_instance.region)
    )
    start_tunnel(new_client, running_instance.instance_id, port)
