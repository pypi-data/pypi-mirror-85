from typing import Optional, Tuple

import click

from ..decorators import loses_interactivity, require_bins, require_login
from ..helpers.ansible import run_ansible
from ..helpers.global_options import GlobalOptions
from ..helpers.options import ansible_options, resource_argument
from .sym import sym


@sym.command(
    short_help="Run an Ansible command",
    context_settings={"ignore_unknown_options": True},
)
@resource_argument
@click.argument("command", nargs=-1)
@ansible_options
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("ansible", "aws", "session-manager-plugin")
@require_login
def ansible(
    options: GlobalOptions,
    resource: str,
    command: Tuple[str, ...],
    ansible_aws_profile: Optional[str],
    ansible_sym_resource: Optional[str],
    control_master: bool,
    send_command: bool,
    forks: int,
) -> None:
    """Run Ansible commands against an inventory of EC2 instances, using
    approved credentials from the Sym RESOURCE group.

    For a list of available Sym RESOURCES, run `sym resources`.

    \b
    Example:
        `sym ansible RESOURCE all -m ping`
    """
    client = options.create_saml_client(resource)
    run_ansible(
        client,
        command,
        ansible_aws_profile=ansible_aws_profile,
        ansible_sym_resource=ansible_sym_resource,
        control_master=control_master,
        send_command=send_command,
        forks=forks,
    )
