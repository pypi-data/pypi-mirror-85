import requests
import pytest
from botocore.exceptions import ClientError

from metadata_driver_aws.data_plugin import Plugin


@pytest.mark.xfail(raises=ClientError)
def test_generate_url():
    config = dict()  #
    s3_plugin = Plugin(config)

    sign_url = s3_plugin.generate_url(
        's3://nemermined-metadata-driver-cluster/data.txt')
    assert requests.get(sign_url).content == b'1 2\n2 3\n3 4\n'
