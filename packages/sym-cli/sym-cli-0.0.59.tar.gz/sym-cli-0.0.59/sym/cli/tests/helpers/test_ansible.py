import pytest
from _pytest.monkeypatch import MonkeyPatch
from expects import *

from sym.cli.helpers import params
from sym.cli.helpers.ansible import get_ansible_bucket_name
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.commands.test_ansible import TEST_ACCOUNT, get_caller_identity_stub


@pytest.fixture
def ansible_bucket_foo(monkeypatch: MonkeyPatch):
    new_params = params.PARAMS.copy()
    test = new_params["sym"]["profiles"]["test"]
    new_params["sym"]["profiles"]["test"] = test._replace(ansible_bucket="foo")
    monkeypatch.setattr(params, "PARAMS", new_params)


def test_get_default_ansible_bucket_name(boto_stub, saml_client: SAMLClient):
    get_caller_identity_stub(boto_stub)
    actual = get_ansible_bucket_name(saml_client)
    expect(actual).to(match(f"sym-ansible-{TEST_ACCOUNT}"))


def test_get_ansible_bucket_name(ansible_bucket_foo, boto_stub, saml_client: SAMLClient):
    actual = get_ansible_bucket_name(saml_client)
    expect(actual).to(match("foo"))
