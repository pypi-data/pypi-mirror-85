from datetime import datetime

import pytest
from _pytest.monkeypatch import MonkeyPatch
from expects import *

from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.saml_clients import aws_profile
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.saml_clients.aws_profile import AwsProfile
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox

PROFILE = "foobar"


@pytest.fixture
def write_creds_tester(
    env_creds, command_tester, sandbox: Sandbox, monkeypatch: MonkeyPatch
):
    credentials_path = sandbox.path / ".aws" / "credentials"
    credentials_path.parent.mkdir(parents=True)
    credentials_path.touch()

    monkeypatch.setattr(aws_profile, "AwsCredentialsPath", credentials_path)

    return command_tester(
        [
            "write-creds",
            "test",
            "--profile",
            PROFILE,
            "--path",
            str(credentials_path),
        ]
    )


def test_write_creds_no_login(command_login_tester):
    command_login_tester(["write-creds"])
    command_login_tester(["write-creds", "test"])
    command_login_tester(["write-creds"], {"SYM_RESOURCE": "test"})
    command_login_tester(["write-creds"], {"ENVIRONMENT": "test"})


def test_write_creds(
    creds_env,
    write_creds_tester,
    capture_command: CaptureCommand,
):
    with write_creds_tester():
        capture_command.assert_command(
            ["exec", "true"],
            ["ssh-keygen"],
        )

        client = AwsProfile(PROFILE, options=GlobalOptions())
        expect(client.get_creds()).to(have_keys(creds_env))


def test_write_creds_expiring(
    creds_env,
    write_creds_tester,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
    monkeypatch: MonkeyPatch,
):
    def setup(_make_stub):
        def get_creds(self):
            return {
                **creds_env,
                "AWS_CREDENTIAL_EXPIRATION": datetime.now().isoformat(),
            }

        monkeypatch.setattr(AwsOkta, "get_creds", get_creds)

    with write_creds_tester(setup=setup):
        capture_command.assert_command(
            ["exec", "false"],  # first refresh (loses_interactivity)
            ["exec", "true"],
            ["exec", "false"],  # second refresh (write_creds)
            ["exec", "true"],
            ["ssh-keygen"],
        )

        client = AwsProfile(PROFILE, options=GlobalOptions())
        expect(client.get_creds()).to(have_keys(creds_env))
