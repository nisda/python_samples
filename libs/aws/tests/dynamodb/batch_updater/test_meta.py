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



def test_updater_trasaction():
    _test_meta_handler(transaction=True)


def test_updater_batch():
    _test_meta_handler(transaction=False)


def _test_meta_handler(transaction:bool):

    # テーブル初期化
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME, region_name=TABLE_REGION)
    table.truncate()

    # アップデータ生成
    updater:DynamoBatchUpdater = DynamoBatchUpdater(region_name=TABLE_REGION)


    #-------------------------
    # meta設定 なし
    #-------------------------
    ret = updater.put_items(table_name=TABLE_NAME, items=[ {"pk": "A", "sk": "1", "step": "1"} ])
    ret = updater.commit(transaction=transaction)
    ret = table.get_item(key={"pk": "A", "sk": "1"})
    assert ret.items() == {"pk": "A", "sk": "1", "step": "1"}.items()


    #-------------------------
    # meta設定 追加。デフォルト動作
    #-------------------------
    ret = updater.set_meta_config(table_name=TABLE_NAME)
    ret = updater.put_items(table_name=TABLE_NAME, items=[ {"pk": "A", "sk": "2", "step": "2"} ])
    ret = updater.commit(transaction=transaction)

    ret = table.get_item(key={"pk": "A", "sk": "2"})
    assert ret.items() >= {"pk": "A", "sk": "2", "step": "2"}.items()
    assert ret.get("updated_at", None) is not None


    #-------------------------
    # meta設定 を後から追加⇒反映される。デフォルト動作
    #-------------------------
    updater:DynamoBatchUpdater = DynamoBatchUpdater(region_name=TABLE_REGION)

    ret = updater.put_items(table_name=TABLE_NAME, items=[ {"pk": "A", "sk": "2", "step": "2"} ])
    ret = updater.set_meta_config(table_name=TABLE_NAME)
    ret = updater.commit(transaction=transaction)
    ret = table.get_item(key={"pk": "A", "sk": "2"})
    assert ret.items() >= {"pk": "A", "sk": "2", "step": "2"}.items()
    assert ret.get("updated_at", None) is not None


    #-------------------------
    # meta設定に変更あり -> 反映される
    #-------------------------
    updater:DynamoBatchUpdater = DynamoBatchUpdater(region_name=TABLE_REGION)
    meta_config:Dict = {
        "ttl_default" :  20,
        "updated_at_attr" : "_updated_at",
        "updated_at_format" : "%Y/%m/%d %H.%M.%S",
        "time_zone" : "UTC",
    }

    ret = updater.put_items(table_name=TABLE_NAME, items=[ {"pk": "A", "sk": "3", "step": "3"} ])
    ret = updater.set_meta_config(table_name=TABLE_NAME, **meta_config)
    ret = updater.commit(transaction=transaction)
    ret = table.get_item(key={"pk": "A", "sk": "3"})
    assert ret.items() >= {"pk": "A", "sk": "3", "step": "3"}.items()
    assert ret.get("updated_at", None) is None
    assert ret.get("_updated_at", None) is not None
    assert "/" in ret.get("_updated_at", None)
    assert "." in ret.get("_updated_at", None)
    assert ret.get("ttl", None) is not None


    #-------------------------
    # put指定の有効性
    #-------------------------
    updater:DynamoBatchUpdater = DynamoBatchUpdater(region_name=TABLE_REGION)

    ret = updater.put_items(table_name=TABLE_NAME, items=[ {"pk": "A", "sk": "4", "step": "4"} ])
    ret = updater.put_items(table_name=TABLE_NAME, items=[ {"pk": "A", "sk": "5", "step": "5"} ], ttl=30)

    ret = updater.set_meta_config(table_name=TABLE_NAME, updated_at_attr="_updated_at")
    ret = updater.commit(transaction=transaction)

    ret = table.get_item(key={"pk": "A", "sk": "4"})
    assert ret.get("_updated_at", None) is not None
    assert ret.get("ttl", None) is None

    ret = table.get_item(key={"pk": "A", "sk": "5"})
    assert ret.get("_updated_at", None) is not None
    assert ret.get("ttl", None) is not None

