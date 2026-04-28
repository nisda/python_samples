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
    [ # step-1: put
        {"id": "001", "seq": "1", "name": "A1", "category": {"id": 1, "name": "cate-K"}},
        {"id": "001", "seq": "2", "name": "A2", "category": {"id": 2, "name": "cate-L"}},
        {"id": "001", "seq": "3", "name": "A3", "category": {"id": 2, "name": "cate-L"}},
        {"id": "002", "seq": "1", "name": "B1", "category": {"id": 1, "name": "cate-K"}},
        {"id": "003", "seq": "1", "name": "C1", "category": {"id": 3, "name": "cate-M"}},
    ],
    [ # step-2: delete
        {"id": "001", "seq": "3", "name": "A3", "category": {"id": 2, "name": "cate-L"}},
        {"id": "002", "seq": "1", "name": "B1", "category": {"id": 1, "name": "cate-K"}},
    ],
    [ # step-3: put
        {"id": "001", "seq": "2", "name": "A2Z", "category": {"id": 9, "name": "cate-Z"}},
        {"id": "002", "seq": "2", "name": "B2",  "category": {"id": 3, "name": "cate-M"}},
    ],
]



ITEM_TEMPLATE = {
    "pk" : "{id}",
    "sk" : "{seq}",
    "content" : {
        "name" : "{name}",
        "category_id" : "{category.id}",
        "category_name" : "{category.name}",
    }
}

def test_updater_trasaction():
    transaction = True

    # テーブル初期化
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME, region_name=TABLE_REGION)
    table.truncate()

    # updater で一括更新
    updater:DynamoBatchUpdater = DynamoBatchUpdater(region_name=TABLE_REGION)

    items = UPDATE_ITEMS
    template = ITEM_TEMPLATE

    # データをスタック
    ret = updater.put_items(table_name=TABLE_NAME, items=items[0], template=template)
    ret = updater.delete_items(table_name=TABLE_NAME, items=items[1], template=template)
    ret = updater.put_items(table_name=TABLE_NAME, items=items[2], template=template)


    # コミット
    ret = updater.commit(transaction=transaction)

    # 結果確認
    records: List[Dict] = list(table.scan())
    records = sorted(records, key=lambda x: (x["pk"], x["sk"]) )
    assert len(records) == 4

    # 内容
    assert records[0] == {"pk": "001", "sk": "1", "content": {"name": "A1", "category_id": 1, "category_name": "cate-K"}}
    assert records[1] == {"pk": "001", "sk": "2", "content": {"name": "A2Z", "category_id": 9, "category_name": "cate-Z"}}
    assert records[2] == {"pk": "002", "sk": "2", "content": {"name": "B2",  "category_id": 3, "category_name": "cate-M"}}
    assert records[3] == {"pk": "003", "sk": "1", "content": {"name": "C1", "category_id": 3, "category_name": "cate-M"}}

