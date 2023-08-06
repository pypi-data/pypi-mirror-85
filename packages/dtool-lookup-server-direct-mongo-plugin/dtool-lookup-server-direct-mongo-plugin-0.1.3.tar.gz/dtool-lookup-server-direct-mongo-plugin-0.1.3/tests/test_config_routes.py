"""Test the /mongo/config blueprint route."""

import json
import dtool_lookup_server_direct_mongo_plugin

from . import tmp_app_with_users  # NOQA

snowwhite_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyZTk0MzMzMi0wZWE5LTQ3MWMtYTUxZS02MjUxNGNlOTdkOGMiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzI2NTM5NywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzI2NTM5NywiaWRlbnRpdHkiOiJzbm93LXdoaXRlIn0.FAoj9M4Tpr9IXIsyuD9eKV3oOpQ4_oRE82v6jqMFOSERaMqfWQgpMlTPSBsoWvnsNhigBYA7NKqqRPZ_bCHh73dMk57s6-VBvxtunQIe-MYtnOP9H4lpIdnceIE-Ji34xCd7kxIp0kADtYLhnJjU6Jesk642P0Ndjc8ePxGAl-l--bLbH_A4a3-U2EuowBSwqAp2q56QuGw6oQpKSKt9_eRSThNBE6zJIClfUeQYeCDCcd1Inh5hgrDBurteicCP8gWyVkyZ0YnjojDMECu7P9vDyy-T4AUem9EIAe_hA1nTMKucW2Ki6xyZLvu0TVlHe9AQVYy0O-suxxlrXIJ5Yw"  # NOQA

def test_config_info_route(tmp_app_with_users):  # NOQA

    headers = dict(Authorization="Bearer " + snowwhite_token)
    r = tmp_app_with_users.get(
        "/mongo/config",
        headers=headers,
    )
    assert r.status_code == 200

    expected_content = {
        'allow_direct_query': True,
        'allow_direct_aggregation': False,
        'version': dtool_lookup_server_direct_mongo_plugin.__version__}

    response = json.loads(r.data.decode("utf-8"))
    assert response == expected_content
