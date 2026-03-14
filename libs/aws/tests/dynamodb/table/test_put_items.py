import pytest
from typing import List, Dict, Any
from dynamodb import DynamoTable
from datetime import datetime
from zoneinfo import ZoneInfo
from pprint import pprint
import time

"""
本来はUnitTestの中でテーブル作成も行うべきであるが、今回は省略する。
すでに適切なレイアウトのテーブルが存在しているものとする。
「適切なレイアウト」の説明も省略する。
"""
TABLE_NAME = "test-20260128"






def test_put_items():
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME, ttl_default=10)

    # 全削除
    table.truncate()

    # 実行前状態を取得＆チェック
    records:List[Dict] = list(table.scan())
    assert len(records) == 0

    # 追加: TTLあり（default）
    items = [
        {'pk': 'ut_put_items', 'sk': '1', 'biko': ''},
        {'pk': 'ut_put_items', 'sk': '2', 'biko': ''},
    ]
    ret = table.put_items(items=items)

    # 追加: TTLなし
    items = [
        {'pk': 'ut_put_items', 'sk': '2', 'biko': 'A'},     # 更新
        {'pk': 'ut_put_items', 'sk': '3', 'biko': ''},
    ]
    ret = table.put_items(items=items, ttl=0)


    # 実行前状態を取得＆チェック
    records:List[Dict] = list(table.scan())
    assert len(records) == 3
    assert records[0]["sk"] == '1'
    assert records[1]["sk"] == '2'
    assert records[2]["sk"] == '3'
    assert records[0].get('ttl', None) is not None
    assert records[1].get('ttl', None) is None
    assert records[2].get('ttl', None) is None


