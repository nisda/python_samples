import pytest
from data_table import DataTable
from pprint import pprint
from datetime import datetime




def test_load_col_oriented():
    """列指向データの読み込み"""

    data = {
        "id"  : [1       ,  2    , 3        , ],
        "name": ["Alice" , "Bob" , "Charlie", ],
        "sex" : ["F"     , None  , "M"      , ],
        "age" : [None    , 22    ,            ],  # データの不足は None で埋められる
    }

    # カラム、データの確認
    dt1 = DataTable(data=data)
    dt2 = dt1.clone()

    # 異なるオブジェクト
    assert id(dt1) != id(dt2)

    # 同じ内容
    assert dt1.row_count == dt2.row_count
    assert dt1.column_count == dt2.column_count
    assert dt1.columns == dt2.columns

    # データ変更が元のテーブルには反映されないこと
    dt2["add"] = 1
    assert dt1.column_count != dt2.column_count
    assert dt1.columns != dt2.columns






def test_load_row_oriented_list_no_column():
    """行指向データ(list)の読み込み（列名なし）"""

    data = [
        [1, "Alice", "F"],
        [2, "Bob", None, 22],
        [3, "Charlie", "M", None],
    ]

    # カラム、データの確認
    dt1 = DataTable(data=data)
    dt2 = dt1.clone()

    # 異なるオブジェクト
    assert id(dt1) != id(dt2)

    # 同じ内容
    assert dt1.row_count == dt2.row_count
    assert dt1.column_count == dt2.column_count
    assert dt1.columns == dt2.columns

    # データ変更が元のテーブルには反映されないこと
    dt2["add"] = 1
    assert dt1.column_count != dt2.column_count
    assert dt1.columns == dt2.columns   # 列名を持っていないので同じになる
