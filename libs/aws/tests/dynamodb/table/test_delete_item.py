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






def test_delete_item():
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME, ttl_default=10)

    # 全削除
    table.truncate()

    # 実行前状態を取得＆チェック
    records:List[Dict] = list(table.scan())
    assert len(records) == 0

    # 追加: TTLあり（default）
    put_items = [
        {'pk': 'ut_put_items', 'sk': '1', 'biko': ''},
        {'pk': 'ut_put_items', 'sk': '2', 'biko': ''},
        {'pk': 'ut_put_items', 'sk': '3', 'biko': ''},
        {'pk': 'ut_put_items', 'sk': '4', 'biko': ''},
    ]
    ret = table.put_items(items=put_items)

    # 削除１
    delete_key = {'pk': 'ut_put_items', 'sk': '2'}
    ret = table.delete_item(key=delete_key)
    assert ret is not None

    records:List[Dict] = list(table.scan())
    assert len(records) == 3

    # 削除２
    delete_key = {'pk': 'ut_put_items', 'sk': '4', 'biko': ''}  # キー以外の項目が存在していてもよい
    ret = table.delete_item(key=delete_key)
    assert ret is not None

    # 実行前状態を取得＆チェック
    records:List[Dict] = list(table.scan())
    assert len(records) == 2
    assert records[0]["sk"] == '1'
    assert records[1]["sk"] == '3'

    # 存在しないデータを削除しようとした場合は None
    delete_key = {'pk': 'ut_put_items', 'sk': '4', 'biko': ''}  # キー以外の項目が存在していてもよい
    ret = table.delete_item(key=delete_key)
    assert ret is None
