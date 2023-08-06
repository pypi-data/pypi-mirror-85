import pytest

from metadata_driver_azure.data_plugin import Plugin


@pytest.fixture
def osmo():
    return Plugin('./tests/config.ini')