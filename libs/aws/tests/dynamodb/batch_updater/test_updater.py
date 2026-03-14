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
    [ # put
        {"pk": "A", "sk": "1", "step": 1},
        {"pk": "A", "sk": "2", "step": 1},
        {"pk": "A", "sk": "3", "step": 1},
        # {"pk": "B", "sk": "4", "step": 1},
        # {"pk": "B", "sk": "5", "step": 1},
        # {"pk": "B", "sk": "6", "step": 1},
    ],
    [ # put
        # {"pk": "A", "sk": "1", "step": 2},
        # {"pk": "A", "sk": "2", "step": 2},
        {"pk": "A", "sk": "3", "step": 2},
        {"pk": "B", "sk": "4", "step": 2},
        # {"pk": "B", "sk": "5", "step": 2},
        # {"pk": "B", "sk": "6", "step": 2},
    ],
    [ # delete
        # {"pk": "A", "sk": "1", "step": 3},
        # {"pk": "A", "sk": "2", "step": 3},
        # {"pk": "A", "sk": "3", "step": 3},
        {"pk": "B", "sk": "4", "step": 3},
        {"pk": "B", "sk": "5", "step": 3},
        {"pk": "B", "sk": "6", "step": 3},
    ],
    [ # put
        {"pk": "A", "sk": "1", "step": 4},
        # {"pk": "A", "sk": "2", "step": 4},
        # {"pk": "A", "sk": "3", "step": 4},
        {"pk": "B", "sk": "4", "step": 4},
        # {"pk": "B", "sk": "5", "step": 4},
        {"pk": "B", "sk": "6", "step": 4},
    ],
]


def test_updater_trasaction():
    transaction = True

    # テーブル初期化
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME, region_name=TABLE_REGION)
    table.truncate()

    # updater で一括更新
    updater:DynamoBatchUpdater = DynamoBatchUpdater(region_name=TABLE_REGION)

    items = UPDATE_ITEMS

    # Step 1, 2
    ret = updater.put_items(table_name=TABLE_NAME, items=items[0])
    ret = updater.put_items(table_name=TABLE_NAME, items=items[1])
    ret = updater.commit(transaction=transaction)
    records: List[Dict] = list(table.scan())
    assert len(records) == 4

    # Step 3, 4
    ret = updater.delete_items(table_name=TABLE_NAME, items=items[2])
    ret = updater.put_items(table_name=TABLE_NAME, items=items[3])
    ret = updater.commit(transaction=transaction)
    records: List[Dict] = list(table.scan())
    assert len(records) == 5

    # 内容
    assert records[0].items() == {"pk": "A", "sk": "1", "step": 4}.items()
    assert records[1].items() == {"pk": "A", "sk": "2", "step": 1}.items()
    assert records[2].items() == {"pk": "A", "sk": "3", "step": 2}.items()
    assert records[3].items() == {"pk": "B", "sk": "4", "step": 4}.items()
    assert records[4].items() == {"pk": "B", "sk": "6", "step": 4}.items()



def test_updater_batch():
    transaction = False

    # テーブル初期化
    table:DynamoTable = DynamoTable(table_name=TABLE_NAME, region_name=TABLE_REGION)
    table.truncate()

    # updater で一括更新
    updater:DynamoBatchUpdater = DynamoBatchUpdater(region_name=TABLE_REGION)

    items = UPDATE_ITEMS

    # Step 1, 2
    ret = updater.put_items(table_name=TABLE_NAME, items=items[0])
    ret = updater.put_items(table_name=TABLE_NAME, items=items[1])
    ret = updater.commit(transaction=transaction)
    records: List[Dict] = list(table.scan())
    assert len(records) == 4

    # Step 3, 4
    ret = updater.delete_items(table_name=TABLE_NAME, items=items[2])
    ret = updater.put_items(table_name=TABLE_NAME, items=items[3])
    ret = updater.commit(transaction=transaction)
    records: List[Dict] = list(table.scan())
    assert len(records) == 5

    # 内容
    assert records[0].items() == {"pk": "A", "sk": "1", "step": 4}.items()
    assert records[1].items() == {"pk": "A", "sk": "2", "step": 1}.items()
    assert records[2].items() == {"pk": "A", "sk": "3", "step": 2}.items()
    assert records[3].items() == {"pk": "B", "sk": "4", "step": 4}.items()
    assert records[4].items() == {"pk": "B", "sk": "6", "step": 4}.items()
