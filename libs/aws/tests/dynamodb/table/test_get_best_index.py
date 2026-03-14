import pytest
from typing import List,Dict
from pprint import pprint

from dynamodb import DynamoTable
from dynamodb import DynamoIndexTypes
from dynamodb.index import DynamoIndex

TABLE_NAME:str = "test-20260128"


@pytest.mark.parametrize(
    [
        "i_search_keys", "i_range_compare_key", "e_is_match", "e_index_type", "e_index_name",
    ],
    [
        # primary に合致
        pytest.param(["A", "pk"]                             , None, True, DynamoIndexTypes.Primary ,None),
        pytest.param(["A", "pk", "sk"]                       , None, True, DynamoIndexTypes.Primary, None),
        pytest.param(["A", "pk", "sk", "lsi_sk", "gsi_pk1"]  , None, True, DynamoIndexTypes.Primary, None),
        pytest.param(["A", "pk"]                             , "sk", True, DynamoIndexTypes.Primary ,None),
        pytest.param(["A", "pk", "lsi_sk", "gsi_pk1"]        , "sk", True, DynamoIndexTypes.Primary, None),

        # LSI に合致
        pytest.param(["A", "pk", "lsi_sk"]   ,  None, True, DynamoIndexTypes.LSI, "LSI-01"),
        pytest.param(["A", "pk"]             , "lsi_sk", True, DynamoIndexTypes.LSI, "LSI-01"),
        pytest.param(["A", "pk", "lsi_sk"]   , "lsi_sk", True, DynamoIndexTypes.LSI, "LSI-01"),      
        pytest.param(["A", "pk", "sk"]       , "lsi_sk", True, DynamoIndexTypes.LSI, "LSI-01"),  # range_compare_key優先

        # GSI1 に合致
        pytest.param(["A", "gsi_pk1"]   ,  None, True, DynamoIndexTypes.GSI, "GSI-01"),

        # GSI2 に合致（GSI1にも合致するが、より長い2が優先）
        pytest.param(["A", "gsi_pk1", "gsi_pk2"]            ,  None, True, DynamoIndexTypes.GSI, "GSI-02"),
        pytest.param(["A", "gsi_pk1", "gsi_pk2", "gsi_sk1"] ,  None, True, DynamoIndexTypes.GSI, "GSI-02"),
        pytest.param(["A", "gsi_pk1", "gsi_pk2", "gsi_sk2"] ,  None, True, DynamoIndexTypes.GSI, "GSI-02"), # HASHまでマッチ

        # どれにも合致しない（Range比較キー）
        pytest.param(["A", "gsi_pk1", "gsi_pk2", "gsi_sk1"] ,  "gsi_sk3", False, None, None),
        pytest.param(["A", "gsi_pk1", "gsi_pk2"]            ,  "lsi_sk", False, None, None),

        # どれにも合致しない（HASHキー）
        pytest.param(["A", "lsi_sk"] ,  None, False, None, None),
    ]
)
def test_match(i_search_keys, i_range_compare_key, e_is_match, e_index_type, e_index_name):
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME)

    ret:DynamoIndex = table.get_best_index(
        search_keys=i_search_keys,
        range_compare_key=i_range_compare_key
    )

    if e_is_match:
        assert ret.type == e_index_type
        assert ret.name == e_index_name
    else:
        assert ret is None

