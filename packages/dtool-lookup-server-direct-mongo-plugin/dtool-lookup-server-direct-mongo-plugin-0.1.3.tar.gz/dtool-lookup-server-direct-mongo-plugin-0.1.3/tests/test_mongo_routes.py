"""Test the /mongo blueprint routes."""
# NOTE: modified subset of dtool-lookup-server/tests/dataset_routes.py

import json

from . import tmp_app_with_data, tmp_app_with_data_and_relaxed_security  # NOQA
from . import compare_nested

snowwhite_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyZTk0MzMzMi0wZWE5LTQ3MWMtYTUxZS02MjUxNGNlOTdkOGMiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzI2NTM5NywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzI2NTM5NywiaWRlbnRpdHkiOiJzbm93LXdoaXRlIn0.FAoj9M4Tpr9IXIsyuD9eKV3oOpQ4_oRE82v6jqMFOSERaMqfWQgpMlTPSBsoWvnsNhigBYA7NKqqRPZ_bCHh73dMk57s6-VBvxtunQIe-MYtnOP9H4lpIdnceIE-Ji34xCd7kxIp0kADtYLhnJjU6Jesk642P0Ndjc8ePxGAl-l--bLbH_A4a3-U2EuowBSwqAp2q56QuGw6oQpKSKt9_eRSThNBE6zJIClfUeQYeCDCcd1Inh5hgrDBurteicCP8gWyVkyZ0YnjojDMECu7P9vDyy-T4AUem9EIAe_hA1nTMKucW2Ki6xyZLvu0TVlHe9AQVYy0O-suxxlrXIJ5Yw"  # NOQA

grumpy_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5NjJjODEyNi1kZDJlLTQ1NDEtODQyOC0yZDYxYjEwZmU0M2YiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzIyMzEzMywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzIyMzEzMywiaWRlbnRpdHkiOiJncnVtcHkifQ.K1YYcUp2jfpBhVd7ggBJ_mpnQT_ZAGRjfgrReoz9no6zZ_5Hlgq2YLUNFtFfr2PrqsaO5fKWUfKrR8bjMijtlRlAEmyCJvalqXDWvriMf2QowyR6IjKxSNZcVCMkJXEk7cRlEM9f815YABc3RsG1F75n2dV5NSuvcQ4dQoItvNYpsuHZ3c-xYQuaQt7_Ch50Ez-H2fJatXQYdnHruyZOJQKPIssxU_yyeCnlOGklCmDn8mIolQEChrvW9HhpvgXsaAWEHjtNRK4T_ZH37Dq44fIB9ax6GGRZHDjWmjOicrGolfu73BuI8fOpLLpW5af6SKP-UhZA4AcW_TYG4PnOpQ"  # NOQA

sleepy_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhNzBhNmQ1ZS0xMTU4LTQ5YzAtOGM0OS02MmU1MzYzZWM3NDQiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzIyMzIyNCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzIyMzIyNCwiaWRlbnRpdHkiOiJzbGVlcHkifQ.o15vGkZVsP_RaCIwXljFrkmFTef7ToPo_ssg7DPzRc33LhZh352gn6kY90JGMD1eyvrw69u6RwKW_5RkBmkDweCExiSDx7EuEofgadEegkM9qfbRfPGRpihobmQmwDADc6qspROUDi__gjrALLFZvg8cAteBVOBhKrItwHADym4RCHzDTyP0dd-k8PzvKUqBxryK5yutpc5Tkju3Bg33bFIyjJTr9kzZbjnzoYSjl1Nb7YtCO6ijsJasIPfLK8OOB2kza9NrAOAhWKqWtynzkyCCVckicfGZI5ywzNlsUqGcQwb7fNMUR-1JErM0wGViKOmotcQ08ut69KM5p8XZmg"  # NOQA

dopey_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0MTIxZDhhYi1iYjg5LTRlYTgtOTg3Zi0zYjgyOTc2ODkwZjEiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzIyMzM0MCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzIyMzM0MCwiaWRlbnRpdHkiOiJkb3BleSJ9.K8MeDodbdwDN2ErspmWgQJCra3EXdpIrsyWQVqCNZNKsjUZsYLNAetzqJe71NhiVFuoaqDm0ta9jNnQE5NpehQSFv0SveMPu4wIaVpcCDQXHOYGGljbhHa18v0dEZibZFEYnMwY_b0VWtpzXZXZSYiLVMD2kcnUqXouV7fPXlSp5SuFCEh5Y6rw0nZqxMTVdbDvZLm2rxjJI_4GHMj1KMpsGKYGTxniA1iWvR9WionJOdDxn5gc8roDERGuSQpm4LCQxz_WJk8pNX4IdQgPuz6TVNsXnUnD2LiGe9Dz8q-FstcTwRy2u97l76OgCGSf7vkhELHTqRj32cEdxnPNpTA"  # NOQA

noone_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhMzUwY2MwZS1jMzAyLTQ1MGItYTE0NC01YTQzZjE3MDc4NDkiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzI3NzA1MCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzI3NzA1MCwiaWRlbnRpdHkiOiJub29uZSJ9.VCRRsfLM5mwYz_viMVAJzfLf3_IF7MDTyzeWv3Ae_YYumu3UQVXUqWqJnvwyAY7KAqEIWkoFUET_bp-48WrvGaGr8q355IXiqspURpMMCLQ4G7Jwm3EnN6I61e_C6XpoyliZnd06qiVZR5VuaHxk41XclwRwgPCsEflj30SKWgVQOGbOYFfcSEdMKUvu8fyGbRwo47ynHvHrmxMAuURWjnN3g8gD-shBHCt1_4GVDSp1LSipSysDcn3-SdFa0PLGZqQ4Xj7QzM7AMmZ20J0uSHVA5U6RBzLU8d_neDdAg-Y2sjAC_G2P7jj0RdIU-QlDx2B25nyr4rOO9oSOI_q54Q"  # NOQA


def test_mongo_query_route(tmp_app_with_data):  # NOQA
    headers = dict(Authorization="Bearer " + grumpy_token)

    # first, just repeat all tests from test_dataset_search_route
    # without any raw query specified, query should behave equivalenty
    # to search.
    query = {}  # Everything.
    r = tmp_app_with_data.post(
        "/mongo/query",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 3

    r = tmp_app_with_data.post(
        "/mongo/query",
        headers=dict(Authorization="Bearer " + sleepy_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 0

    r = tmp_app_with_data.post(
        "/mongo/query",
        headers=dict(Authorization="Bearer " + dopey_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 401

    r = tmp_app_with_data.post(
        "/mongo/query",
        headers=dict(Authorization="Bearer " + noone_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 401

    # Search for apples (in README).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "apple"}
    r = tmp_app_with_data.post(
        "/mongo/query",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 2

    # Search for U00096 (in manifest).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "U00096"}
    r = tmp_app_with_data.post(
        "/mongo/query",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 2

    # Search for crazystuff (in annotaitons).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "crazystuff"}
    r = tmp_app_with_data.post(
        "/mongo/query",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 1

    # second, try some direct mongo
    query = {
        'query': {
            'base_uri': 's3://snow-white',
            'readme.descripton': {'$regex': 'from queen'},
        }
    }
    r = tmp_app_with_data.post(
        "/mongo/query",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 2


def test_mongo_aggregate_route(tmp_app_with_data_and_relaxed_security):  # NOQA
    headers = dict(Authorization="Bearer " + grumpy_token)

    # first, just repeat all tests from test_dataset_search_route
    # without any aggregation specified, aggregate should behave equivalenty
    # to search.
    query = {}  # Everything.
    r = tmp_app_with_data_and_relaxed_security.post(
        "/mongo/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 3

    r = tmp_app_with_data_and_relaxed_security.post(
        "/mongo/aggregate",
        headers=dict(Authorization="Bearer " + sleepy_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 0

    r = tmp_app_with_data_and_relaxed_security.post(
        "/mongo/aggregate",
        headers=dict(Authorization="Bearer " + dopey_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 401

    r = tmp_app_with_data_and_relaxed_security.post(
        "/mongo/aggregate",
        headers=dict(Authorization="Bearer " + noone_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 401

    # Search for apples (in README).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "apple"}
    r = tmp_app_with_data_and_relaxed_security.post(
        "/mongo/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 2

    # Search for U00096 (in manifest).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "U00096"}
    r = tmp_app_with_data_and_relaxed_security.post(
        "/mongo/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 2

    # Search for crazystuff (in annotaitons).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "crazystuff"}
    r = tmp_app_with_data_and_relaxed_security.post(
        "/mongo/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 1

    # second, try some direct aggregation
    query = {
        'aggregation': [
            {
                '$sort': {'base_uri': 1}
            }, {
                '$group':  {
                    '_id': '$name',
                    'count': {'$sum': 1},
                    'available_at': {'$push': '$base_uri'}
                }
            }, {
                '$project': {
                    'name': '$_id',
                    'count': True,
                    'available_at': True,
                    '_id': False,
                }
            }, {
                '$sort': {'name': 1}
            }
        ]
    }
    r = tmp_app_with_data_and_relaxed_security.post(
        "/mongo/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    expected_response = [
        {
            'available_at': ['s3://mr-men', 's3://snow-white'],
            'count': 2,
            'name': 'bad-apples'
        }, {
            'available_at': ['s3://snow-white'],
            'count': 1,
            'name': 'oranges'
        }
    ]
    response = json.loads(r.data.decode("utf-8"))
    assert compare_nested(response, expected_response)
