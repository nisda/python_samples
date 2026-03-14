import pytest
from dynamodb import DynamoTable
import sys
from pprint import pprint
from datetime import datetime
import time

"""
本来はUnitTestの中でテーブル作成も行うべきであるが、今回は省略する。
すでに適切なレイアウトのテーブルが存在しているものとする。
「適切なレイアウト」の説明も面倒なので省略する。
"""
TABLE_NAME = "test-20260128"



@pytest.mark.parametrize(
    [
        "i_key_items",
    ],
    [
        # Primary
        pytest.param({"pk": "ut_put", }),
        pytest.param({"pk": "ut_put", "sk": "overwrite", "biko": "A"}),

        # LSI
        pytest.param({"pk": "ut_put", "lsi_sk": "X", "biko": "A"}),

        # GSI
        pytest.param({"gsi_pk1": "a", "gsi_sk1": "X", "biko": "A"}),

        # GSI
        pytest.param({"gsi_pk1": "a", "gsi_sk1": "X", "gsi_pk2": "A"}),
        pytest.param({"gsi_pk1": "a", "gsi_sk1": "X", "gsi_sk3": "A"}),
    ]
)
def test_query2(i_key_items):
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME)

    ret = list(table.query2(key_items=i_key_items))
    print(len(ret))
