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


def test_query2():
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME)

    i_key_items = [
        {"pk": "ut_put", "sk": "overwrite"},
        {"pk": "ut_put", "sk": "different key"},
        {"pk": "PartiQL", "sk": "Test2"},
    ]

    ret = table.query2(key_items=i_key_items)
    print(type(ret))
    for x in ret:
         print(type(x))
         print(x)
