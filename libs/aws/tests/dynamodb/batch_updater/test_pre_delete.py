import pytest
import boto3

from typing import List, Dict, Any
from boto3.dynamodb.conditions import AttributeBase, Key, Attr, Or, And, Not
from dynamodb import DynamoBatchUpdater
from dynamodb import DynamoTable
from pprint import pprint
from datetime import datetime


TABLE_NAME = "test-20260128"
TABLE_REGION = "ap-northeast-1"

UPDATE_ITEMS:List[List[Dict]] = [
    # 既存データ
    [
        {"pk": "A", "sk": "1", "name": "A1"},   # 事前削除
        {"pk": "A", "sk": "2", "name": "A2"},   # 事前削除
        {"pk": "A", "sk": "3", "name": "A3"},   # 事前削除
        {"pk": "A", "sk": "4", "name": "A4"},   # 事前削除
        {"pk": "B", "sk": "1", "name": "B1"},
        {"pk": "B", "sk": "2", "name": "B2"},
        {"pk": "B", "sk": "3", "name": "B3"},   # 事前削除
        {"pk": "C", "sk": "1", "name": "C1"}, 
        {"pk": "C", "sk": "2", "name": "C2"},
    ],
    # 事前削除(pre-delete)  *** テスト対象
    [
        {"pk": "A"},
        {"pk": "B", "sk": "3"},
    ],
    # 追加更新1
    [
        {"pk": "A", "sk": "1", "name": "A1_"},  # 事前削除 -> 追加１
        {"pk": "B", "sk": "4", "name": "B4_"},  # 追加１
        {"pk": "C", "sk": "1", "name": "C1_"},  # 更新１
    ],
    # 削除
    [
        {"pk": "C", "sk": "2", "name": "C2_xx"},   # 削除
    ],
    # 追加更新２
    [
        {"pk": "A", "sk": "2", "name": "A2__"},  # 事前削除 -> 追加２
        {"pk": "B", "sk": "2", "name": "B2__"},  # 更新２
    ],
    # 想定結果
    [
        {"pk": "A", "sk": "1", "name": "A1_"},  # 事前削除 -> 追加１
        {"pk": "A", "sk": "2", "name": "A2__"},  # 事前削除 -> 追加２
        {"pk": "B", "sk": "1", "name": "B1"},
        {"pk": "B", "sk": "2", "name": "B2__"},  # 更新２
        {"pk": "B", "sk": "4", "name": "B4_"},  # 追加１
        {"pk": "C", "sk": "1", "name": "C1_"},  # 更新１
    ],
]


def test_updater_trasaction():
    transaction = True
    items = UPDATE_ITEMS

    # テーブル＆Updaterオブジェクト生成
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME, region_name=TABLE_REGION)
    updater:DynamoBatchUpdater = DynamoBatchUpdater(region_name=TABLE_REGION)

    #-----------------------------------
    #   その１
    #-----------------------------------

    # 既存データ登録
    table.truncate()
    ret = updater.put_items(table_name=TABLE_NAME, items=items[0])      # 既存データ
    ret = updater.commit(transaction=transaction)
    records: List[Dict] = list(table.scan())
    assert len(records) == len(items[0])

    # 登録更新処理
    ret = updater.pre_delete(table_name=TABLE_NAME, condition=items[1]) # 事前削除
    ret = updater.put_items(table_name=TABLE_NAME, items=items[2])
    ret = updater.delete_items(table_name=TABLE_NAME, items=items[3])
    ret = updater.put_items(table_name=TABLE_NAME, items=items[4])
    ret = updater.commit(transaction=transaction)

    # 確認
    records: List[Dict] = list(table.scan())
    assert len(records) == len(items[5])
    assert records == items[5]



    #-----------------------------------
    #   pre_delete の順番を最後に
    #-----------------------------------

    # 既存データ登録
    table.truncate()
    ret = updater.put_items(table_name=TABLE_NAME, items=items[0])      # 既存データ
    ret = updater.commit(transaction=transaction)
    records: List[Dict] = list(table.scan())
    assert len(records) == len(items[0])

    # 登録更新処理
    ret = updater.put_items(table_name=TABLE_NAME, items=items[2])
    ret = updater.delete_items(table_name=TABLE_NAME, items=items[3])
    ret = updater.put_items(table_name=TABLE_NAME, items=items[4])
    ret = updater.pre_delete(table_name=TABLE_NAME, condition=items[1]) # 事前削除
    ret = updater.commit(transaction=transaction)

    # 確認
    records: List[Dict] = list(table.scan())
    assert len(records) == len(items[5])
    assert records == items[5]



    #-----------------------------------
    #  pre_delete の順番を途中に
    #-----------------------------------

    # 既存データ登録
    table.truncate()
    ret = updater.put_items(table_name=TABLE_NAME, items=items[0])      # 既存データ
    ret = updater.commit(transaction=transaction)
    records: List[Dict] = list(table.scan())
    assert len(records) == len(items[0])

    # 登録更新処理
    ret = updater.put_items(table_name=TABLE_NAME, items=items[2])
    ret = updater.delete_items(table_name=TABLE_NAME, items=items[3])
    ret = updater.pre_delete(table_name=TABLE_NAME, condition=items[1]) # 事前削除
    ret = updater.put_items(table_name=TABLE_NAME, items=items[4])
    ret = updater.commit(transaction=transaction)

    # 確認
    records: List[Dict] = list(table.scan())
    assert len(records) == len(items[5])
    assert records == items[5]





