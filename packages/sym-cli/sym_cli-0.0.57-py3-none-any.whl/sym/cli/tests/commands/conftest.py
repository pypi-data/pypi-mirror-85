from contextlib import contextmanager
from typing import Sequence

import pytest
from expects import *

from sym.cli.helpers.contexts import push_envs
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox
from sym.cli.tests.matchers import fail_with, succeed


@pytest.fixture
def command_login_tester(click_setup):
    def tester(args, envs={}):
        with click_setup(set_org=False) as runner:
            with push_envs(envs):
                result = runner.invoke(click_command, args)
                assert result.exit_code > 0
                assert "Error: Please run `sym login` first" in result.output

    return tester


@pytest.fixture
def command_tester(
    click_context,
    click_setup,
    ssm_bins,
    env_creds,
    boto_stub,
    saml_client: SAMLClient,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def tester(command: Sequence[str], setup=None, **kwargs):
        stubs = []

        def make_stub(service):
            stub = boto_stub(service)
            stubs.append(stub)
            return stub

        if setup:
            setup()

        teardown_ = kwargs.get("teardown")

        @contextmanager
        def context(setup=None, teardown=None, exception=None):
            with click_setup() as runner:
                with click_context:
                    if setup:
                        setup(make_stub)

                with capture_command():
                    result = runner.invoke(click_command, command, catch_exceptions=False)
                    if exception:
                        expect(result).to(fail_with(exception))
                    else:
                        expect(result).to(succeed())
                    yield result

                for stub in stubs:
                    stub.assert_no_pending_responses()

                if teardown:
                    teardown()
                if teardown_:
                    teardown_()

        return context

    return tester
