import pytest

from sym.cli.helpers.config import Config
from sym.cli.helpers.ec2.cache import CachingEc2Client
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.helpers.ec2.conftest import (
    BOTO_INSTANCE_RESPONSE,
    DEFAULT_REGION,
    TEST_INSTANCE,
    TEST_INSTANCE_ID,
    TEST_IP,
)
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def caching_ec2_client(saml_client: SAMLClient) -> CachingEc2Client:
    return CachingEc2Client(saml_client)


def test_cache_miss_then_hit_id(
    sandbox: Sandbox, caching_ec2_client: CachingEc2Client, ec2_stub
):
    with sandbox.push_xdg_config_home():
        ec2_stub.add_response(
            "describe_instances",
            BOTO_INSTANCE_RESPONSE,
        )
        instance = caching_ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)
        assert instance == TEST_INSTANCE

        cached = Config.get_servers()
        assert len(cached) == 1

        cached_instance = cached[TEST_INSTANCE_ID]
        assert cached_instance["region"] == DEFAULT_REGION
        assert cached_instance["aliases"] == []
        assert cached_instance["last_connection"] == None

        reloaded_instance = caching_ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)
        assert instance == reloaded_instance


def test_cache_miss_then_hit_by_ip(
    sandbox: Sandbox, caching_ec2_client: CachingEc2Client, ec2_stub
):
    with sandbox.push_xdg_config_home():
        ec2_stub.add_response(
            "describe_instances",
            BOTO_INSTANCE_RESPONSE,
        )
        instance = caching_ec2_client.load_instance_by_alias(TEST_IP)
        assert instance == TEST_INSTANCE

        cached = Config.get_servers()
        assert len(cached) == 1

        cached_instance = cached[TEST_INSTANCE_ID]
        assert cached_instance["region"] == DEFAULT_REGION
        assert cached_instance["aliases"] == [TEST_IP]
        assert cached_instance["last_connection"] == None

        reloaded_instance = caching_ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)
        assert instance == reloaded_instance
