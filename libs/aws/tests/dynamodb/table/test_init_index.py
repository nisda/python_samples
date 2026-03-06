from dynamodb import dynamodb_util
from dynamodb.dynamodb_util import IndexTypes
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



def test_index_init():
    table:dynamodb_util.Table = dynamodb_util.Table(table_name=TABLE_NAME)
    pk = table.pk
    assert pk.name      is None
    assert pk.type      == IndexTypes.Primary
    assert pk.hash_keys  == ["pk"]
    assert pk.range_keys == ["sk"]

    lsi_01 = table.lsi["LSI-01"]
    assert lsi_01.name       == "LSI-01"
    assert lsi_01.type       == IndexTypes.LSI
    assert lsi_01.hash_keys  == ["pk"]
    assert lsi_01.range_keys == ["lsi_sk"]

    gsi_01 = table.gsi["GSI-01"]
    assert gsi_01.name       == "GSI-01"
    assert gsi_01.type       == IndexTypes.GSI
    assert gsi_01.hash_keys  == ["gsi_pk1"]
    assert gsi_01.range_keys == []

    gsi_02 = table.gsi["GSI-02"]
    assert gsi_02.name       == "GSI-02"
    assert gsi_02.type       == IndexTypes.GSI
    assert gsi_02.hash_keys  == ["gsi_pk1", "gsi_pk2"]
    assert gsi_02.range_keys == ["gsi_sk1", "gsi_sk2", "gsi_sk3"]





