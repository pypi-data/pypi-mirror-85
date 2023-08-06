import os

import pytest

from metadata_driver_azure.data_plugin import Plugin
from metadata_driver_azure.data_plugin import _parse_url
from metadata_driver_interface.exceptions import DriverError


@pytest.mark.xfail(raises=DriverError)
def test_copy_file(osmo):
    assert osmo.type() == 'Azure'


# To run this test you need to login with your credentials through az login
@pytest.mark.xfail(raises=DriverError)
def test_list(osmo):
    osmo.upload('./LICENSE', 'https://testocnfiles.blob.core.windows.net/metadata-driver/license_copy')
    osmo.download('https://testocnfiles.blob.core.windows.net/metadata-driver/license_copy', 'license_copy')
    assert open('license_copy').read() == open('./LICENSE').read()
    assert 'license_copy' in osmo.list('metadata-driver', True, 'testocnfiles')
    assert osmo.generate_url('https://testocnfiles.blob.core.windows.net/metadata-driver/license_copy')
    osmo.delete('https://testocnfiles.blob.core.windows.net/metadata-driver/license_copy')
    os.remove('license_copy')

@pytest.mark.xfail(raises=DriverError)
def test_files_share(osmo):
    osmo.upload('./LICENSE', 'https://testocnfiles.file.core.windows.net/metadata-driver/license_copy')
    osmo.download('https://testocnfiles.file.core.windows.net/metadata-driver/license_copy', 'license_copy')
    assert open('license_copy').read() == open('./LICENSE').read()
    assert osmo.generate_url('https://testocnfiles.file.core.windows.net/metadata-driver/license_copy')
    assert 'license_copy' in osmo.list('metadata-driver', False, 'testocnfiles')
    osmo.delete('https://testocnfiles.file.core.windows.net/metadata-driver/license_copy')
    os.remove('license_copy')


def test_split_url():
    url = 'https://testocnfiles.blob.core.windows.net/mycontainer/myblob'
    parse_url = _parse_url(url)
    assert parse_url.account == 'testocnfiles'
    assert parse_url.container_or_share_name == 'mycontainer'
    assert parse_url.file == 'myblob'


def test_parse_file_url():
    url = 'https://testocnfiles.file.core.windows.net/compute/subfolder/data.txt'
    parse_url = _parse_url(url)
    assert parse_url.account == 'testocnfiles'
    assert parse_url.container_or_share_name == 'compute'
    assert parse_url.path == 'subfolder'
    assert parse_url.file == 'data.txt'
