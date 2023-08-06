import click

from ..decorators import loses_interactivity, require_bins, require_login
from ..helpers.global_options import GlobalOptions
from ..helpers.options import resource_argument
from .sym import sym


@sym.command(hidden=True, short_help="New SSM Session")
@resource_argument
@click.option(
    "--target", help="target instance id", metavar="<instance-id>", required=True
)
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("aws", "session-manager-plugin")
@require_login
def ssm(options: GlobalOptions, resource: str, target: str) -> None:
    """Use approved creds for RESOURCE to start an SSM session to an EC2 instance"""
    options.create_saml_client(resource).exec(
        "aws", "ssm", "start-session", target=target
    )
