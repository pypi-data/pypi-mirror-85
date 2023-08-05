from contextlib import contextmanager
from pathlib import Path
from typing import Callable, ContextManager, Iterator
from uuid import UUID, uuid4

import boto3
import click
import pytest
from _pytest.monkeypatch import MonkeyPatch
from botocore.stub import Stubber
from click.testing import CliRunner

from sym.cli.helpers import boto
from sym.cli.helpers import os as sym_os
from sym.cli.helpers.config import Config
from sym.cli.helpers.envvar_option import reset_used
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.sym_group import SymGroup
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.saml_clients.aws_profile import AwsProfile
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox

CustomOrgFixture = Callable[[str], ContextManager[None]]


@pytest.fixture(autouse=True)
def patch_is_setup(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(SAMLClient, "check_is_setup", lambda self: ...)


@pytest.fixture(autouse=True)
def patch_execvp(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sym_os, "execvp", lambda client, args: client.exec(*args))


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def uuid() -> UUID:
    return uuid4()


@pytest.fixture
def uuid_factory() -> Callable[[], UUID]:
    return uuid4


@pytest.fixture
def custom_org(monkeypatch: MonkeyPatch) -> CustomOrgFixture:
    @contextmanager
    def custom_org(org: str) -> Iterator[None]:
        with monkeypatch.context() as mp:
            mp.setattr(Config, "get_org", classmethod(lambda cls: org))
            yield

    return custom_org


@pytest.fixture
def capture_command(monkeypatch: MonkeyPatch) -> CaptureCommand:
    return CaptureCommand(monkeypatch)


@pytest.fixture
def click_context(sandbox):
    with sandbox.push_xdg_config_home():
        Config.instance()["org"] = "sym"
        Config.instance()["email"] = "y@symops.io"
        sandbox.create_binary(f"bin/{AwsOkta.binary}")
        with sandbox.push_exec_path():
            with click.Context(click_command) as ctx:
                ctx.ensure_object(GlobalOptions)
                yield ctx


@pytest.fixture
def click_setup(sandbox: Sandbox):
    @contextmanager
    def context(set_org=True, set_client=True):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with sandbox.push_xdg_config_home():
                if set_client:
                    sandbox.create_binary(f"bin/{AwsOkta.binary}")
                with sandbox.push_exec_path():
                    if set_org:
                        Config.instance()["org"] = "sym"
                        Config.instance()["email"] = "y@symops.io"
                    yield runner
        reset_used()

    return context


def _env_str(creds):
    return "\n".join([f"{k}={v}" for k, v in creds.items()]) + "\n"


@pytest.fixture
def creds_env():
    return {
        "AWS_REGION": "us-east-2",
        "AWS_ACCESS_KEY_ID": "ASIA4GNNUMIHHBPSAQC3",
        "AWS_SECRET_ACCESS_KEY": "xxx",
        "AWS_SESSION_TOKEN": "xxx",
        "AWS_OKTA_SESSION_EXPIRATION": "1600494616",
    }


@pytest.fixture
def creds_env_str(creds_env):
    return _env_str(creds_env)


@pytest.fixture
def env_creds(creds_env_str, capture_command: CaptureCommand):
    capture_command.register_output(r"env", creds_env_str)


@pytest.fixture
def fake_creds_env():
    return {
        "AWS_REGION": "foobar",
        "AWS_FOOBAR": "baz",
        "AWS_OKTA_SESSION_EXPIRATION": "1600494616",
    }


@pytest.fixture
def fake_creds_env_str(fake_creds_env):
    return _env_str(fake_creds_env)


@pytest.fixture
def saml_client(sandbox: Sandbox, monkeypatch: MonkeyPatch, creds_env):
    def get_creds(self):
        return dict(creds_env)

    monkeypatch.setattr(AwsOkta, "get_creds", get_creds)

    sandbox.create_binary(f"bin/{AwsOkta.binary}")
    with sandbox.push_exec_path():
        return AwsOkta("test", options=GlobalOptions(debug=False))


@pytest.fixture
def ssm_bins(sandbox: Sandbox):
    for binary in ["aws", "session-manager-plugin", "ssh"]:
        sandbox.create_binary(f"bin/{binary}")


@pytest.fixture
def boto_stub(monkeypatch: MonkeyPatch):
    stubs = {}

    def boto_client(_saml_client, service):
        if service in stubs:
            return stubs[service][0]

        client = boto3.client(service)
        stubber = Stubber(client)
        stubber.activate()

        stubs[service] = (client, stubber)
        return client

    monkeypatch.setattr(boto, "boto_client", boto_client)

    def get_stub(service):
        boto_client(None, service)
        return stubs[service][1]

    return get_stub


@contextmanager
def setup_context():
    with click.Context(click_command) as ctx:
        ctx.obj = GlobalOptions(saml_client_type=AwsProfile)
        yield


def empty_saml_client():
    return AwsProfile("test", options=GlobalOptions())


@pytest.fixture(autouse=True)
def cleanup(request):
    request.addfinalizer(SymGroup.reset_tees)
