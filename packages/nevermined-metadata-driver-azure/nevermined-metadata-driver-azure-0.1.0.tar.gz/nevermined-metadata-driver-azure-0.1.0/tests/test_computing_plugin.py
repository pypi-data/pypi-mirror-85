import pytest

from metadata_driver_azure.data_plugin import Plugin as DataPlugin
from metadata_driver_azure.computing_plugin import Plugin as ComputingPlugin
from metadata_driver_interface.utils import parse_config
from metadata_driver_interface.exceptions import DriverError

@pytest.mark.xfail(raises=DriverError)
def test_compute_on_cloud():
    config = parse_config("./tests/config.ini")
    osm_data = DataPlugin('./tests/config.ini')
    osm_computing = ComputingPlugin('./tests/config.ini')
    elements_before_compute = len(osm_data.list(config.get('azure.share.output'),
                                                False,
                                                config.get('azure.account.name')))
    result_file = osm_computing.exec_container(asset_url="data.txt",
                                               algorithm_url="algo.py",
                                               resource_group_name=config.get(
                                                   'azure.resource_group'),
                                               account_name=config.get('azure.account.name'),
                                               account_key=config.get('azure.account.key'),
                                               share_name_input=config.get(
                                                   'azure.share.input'),
                                               share_name_output=config.get(
                                                   'azure.share.output'),
                                               location=config.get('azure.location'),
                                               # input_mount_point=data.get('input_mount_point'),
                                               # output_mount_point=data.get('output_mount_point'),
                                               docker_image='python:3.6-alpine',
                                               memory=1.5,
                                               cpu=1)
    assert len(osm_data.list(config.get('azure.share.output'),
                             False,
                             config.get('azure.account.name'))) == elements_before_compute + 1
    osm_data.delete('https://testocnfiles.file.core.windows.net/output/' + result_file)
