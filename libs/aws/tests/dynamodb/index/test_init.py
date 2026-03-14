import pytest

from dynamodb.index import DynamoIndex, DynamoIndexTypes
from pprint import pprint



def test_init_keys_1():

    index:DynamoIndex = DynamoIndex(
        table=None,
        name="IDX-01",
        type=DynamoIndexTypes.Primary,
        key_schemas=[
            {"KeyType": "HASH", "AttributeName": "pk1"},
        ]
    )

    assert index.hash_keys  == ["pk1"]
    assert index.range_keys == []
    assert index.all_keys   == ["pk1"]


def test_init_keys_2():

    index:DynamoIndex = DynamoIndex(
        table=None,
        name="IDX-01",
        type=DynamoIndexTypes.GSI,
        key_schemas=[
            {"KeyType": "HASH", "AttributeName": "pk1"},
            {"KeyType": "HASH", "AttributeName": "pk2"},
            {"KeyType": "RANGE", "AttributeName": "sk1"},
            {"KeyType": "RANGE", "AttributeName": "sk2"},
            {"KeyType": "RANGE", "AttributeName": "sk3"},
        ]
    )

    assert index.hash_keys  == ["pk1", "pk2"]
    assert index.range_keys == ["sk1", "sk2", "sk3"]
    assert index.all_keys   == ["pk1", "pk2", "sk1", "sk2", "sk3"]
