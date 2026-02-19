from dynamodb import dynamodb_util
import sys
from pprint import pprint
from datetime import datetime
import time

"""
本来はUnitTestの中でテーブル作成も行うべきであるが、今回は省略する。
すでに適切なレイアウトのテーブルが存在しているものとする。
「適切なレイアウト」の説明も省略する。
"""
TABLE_NAME = "test-20260128"





def test_updated_at():
    table:dynamodb_util.Table = dynamodb_util.Table(table_name=TABLE_NAME)
    item = {'pk': 'ut_put', 'sk': 'updated_at', 'biko': ''}
    ret = table.put_item(item=item)

    now_ymd = datetime.now().strftime("%Y-%m-%d")
    updated_at:str|None = ret.pop("_updated_at", None)

    assert updated_at is not None
    assert updated_at.startswith(now_ymd)
    assert item == ret



def test_updated_at_none():
    table:dynamodb_util.Table = dynamodb_util.Table(table_name=TABLE_NAME, updated_at=None)
    item = {'pk': 'ut_put', 'sk': 'updated_at_none', 'biko': ''}
    ret = table.put_item(item=item)

    updated_at:str|None = ret.get("_updated_at", None)

    assert updated_at is None
    assert item == ret


def test_ttl():
    table:dynamodb_util.Table = dynamodb_util.Table(table_name=TABLE_NAME, ttl_default=10)

    # default が適用される
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl_default', 'biko': ''})
    assert ret.get("ttl", None) >= datetime.now().timestamp() + 9
    assert ret.get("ttl", None) < datetime.now().timestamp() + 11

    # 個別指定すればそれが有効
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl_specify'}, ttl=60)
    assert ret.get("ttl", None) >= datetime.now().timestamp() + 59
    assert ret.get("ttl", None) < datetime.now().timestamp() + 61

    # 個別指定がzeroならばttlなし
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl_specify_zero'}, ttl=0)
    assert ret.get("ttl", None) is None

    # 個別指定が None であれば無視して default 採用
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl_specify_none'}, ttl=None)
    assert ret.get("ttl", None) >= datetime.now().timestamp() + 9
    assert ret.get("ttl", None) < datetime.now().timestamp() + 11

    # item にセットされていたらそれをそのまま登録。上書きしない。
    ttl_ts:int = int(datetime.now().timestamp()) + 30
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl_item', "ttl": ttl_ts}, ttl=60)
    assert ret.get("ttl", None) >= datetime.now().timestamp() + 29
    assert ret.get("ttl", None) < datetime.now().timestamp() + 31



def test_overwrite():
    table:dynamodb_util.Table = dynamodb_util.Table(table_name=TABLE_NAME)
    table.truncate()

    # 上書き可
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'overwrite'}, overwrite=True)
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'overwrite'}, overwrite=True)
    assert isinstance(ret, dict)

    # 上書き不可
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'can not be overwrite'}, overwrite=True)
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'can not be overwrite'}, overwrite=False)
    assert ret is None

    # キーが違えば登録可能
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'different key'}, overwrite=True)
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'different key'}, overwrite=False)
    assert ret is None
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'different key-2'}, overwrite=False)
    assert isinstance(ret, dict)
    ret = table.put_item(item={'pk': 'ut_put1', 'sk': 'different key'}, overwrite=False)
    assert isinstance(ret, dict)

    # ttl を過ぎていたら上書き可能
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl'}, overwrite=True, ttl=2)
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl'}, overwrite=False, ttl=2)    # まだ期限内＝上書き不可
    assert ret is None

    time.sleep(3)
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl'}, overwrite=False, ttl=2)    # 期限切れ=上書き可
    assert isinstance(ret, dict)


    # ttl なしは上書き不可
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl_none_ow'}, overwrite=True, ttl=0)
    time.sleep(3)
    ret = table.put_item(item={'pk': 'ut_put', 'sk': 'ttl_none_ow'}, overwrite=False, ttl=30) 
    assert ret is None


