import pytest
from data_table import DataTable
from pprint import pprint
from datetime import datetime



def test_load_empty_data():
    """空データの読み込み"""

    dt1 = DataTable(data=[])
    assert dt1.row_count == 0
    assert dt1.column_count == 0
    assert dt1.columns == ()

    dt2 = DataTable(data={})
    assert dt2.row_count == 0
    assert dt2.column_count == 0
    assert dt2.columns == ()

    dt3 = DataTable(data=None)
    assert dt3.row_count == 0
    assert dt3.column_count == 0
    assert dt3.columns == ()



def test_load_col_oriented():
    """列指向データの読み込み"""

    data = {
        "id"  : [1       ,  2    , 3        , ],
        "name": ["Alice" , "Bob" , "Charlie", ],
        "sex" : ["F"     , None  , "M"      , ],
        "age" : [None    , 22    ,            ],  # データの不足は None で埋められる
    }

    # カラム、データの確認
    dt = DataTable(data=data)

    assert dt.column_count == 4
    assert dt.columns == ("id", "name", "sex", "age")

    rows = list(dt.rows(type='dict'))
    assert dt.row_count == 3
    assert rows[0] == {"id": 1, "name": "Alice"  , "sex": "F", "age": None}
    assert rows[1] == {"id": 2, "name": "Bob"    , "sex": None, "age": 22}
    assert rows[2] == {"id": 3, "name": "Charlie", "sex": "M", "age": None}



    # カラム、データの確認（カラム指定あり）
    dt = DataTable(data=data, columns=["a", "b", "c", "d"])

    assert dt.column_count == 4
    assert dt.columns == ("a", "b", "c", "d")

    rows = list(dt.rows(type='dict'))
    assert dt.row_count == 3
    assert rows[0] == {"a": 1, "b": "Alice"  , "c": "F", "d": None}




def test_load_row_oriented_dict():
    """行指向データ(dict)の読み込み"""

    data = [
        {"id": 1, "name": "Alice", "sex": "F"},
        {"id": 2, "sex": None, "name": "Bob", "age": 22},
        {"name": "Charlie", "id": 3, "sex": "M", "age": None},
    ]

    # カラム、データの確認
    dt = DataTable(data=data)

    assert dt.column_count == 4
    assert dt.columns == ("id", "name", "sex", "age")

    rows = list(dt.rows(type='dict'))
    assert dt.row_count == 3
    assert rows[0] == {"id": 1, "name": "Alice"  , "sex": "F", "age": None}
    assert rows[1] == {"id": 2, "name": "Bob"    , "sex": None, "age": 22}
    assert rows[2] == {"id": 3, "name": "Charlie", "sex": "M", "age": None}


    # カラム、データの確認（カラム指定あり）
    dt = DataTable(data=data, columns=["a", "b", "c", "d"])

    assert dt.column_count == 4
    assert dt.columns == ("a", "b", "c", "d")

    rows = list(dt.rows(type='dict'))
    assert dt.row_count == 3
    assert rows[0] == {"a": 1, "b": "Alice"  , "c": "F", "d": None}




def test_load_row_oriented_list_no_column():
    """行指向データ(list)の読み込み"""

    data = [
        [1, "Alice", "F"],
        [2, "Bob", None, 22],
        [3, "Charlie", "M", None],
    ]

    # カラム指定なし
    dt = DataTable(data=data)
    assert dt.column_count == 4
    assert dt.columns == ("0", "1", "2", "3")

    rows = dt.rows(type='list')
    assert dt.row_count == len(data)
    assert rows[0] == [1, "Alice", "F", None]
    assert rows[1] == [2, "Bob", None, 22]
    assert rows[2] == [3, "Charlie", "M", None]

    # カラム指定あり
    dt = DataTable(data=data, columns=["a", "b", "c", "d"])
    assert dt.column_count == 4
    assert dt.columns == ("a", "b", "c", "d")

    rows = dt.rows(type='dict')
    assert dt.row_count == len(data)
    assert rows[0] == {"a": 1, "b": "Alice", "c": "F", "d": None}



def test_load_line():
    """リスト読み込み"""
    
    data = [
        "A-line",
        "B-line",
        "C-line"
    ]

    # カラム、データの確認
    dt = DataTable(data=data)
    assert dt.column_count == 1
    assert dt.columns == ('0', )

    rows = dt.rows(type='list')
    assert dt.row_count == len(data)
    assert rows[0] == [data[0],]
    assert rows[1] == [data[1],]
    assert rows[2] == [data[2],]

    rows = dt.rows(type='dict')
    assert rows[0] == {'0': data[0], }



def test_load_one():
    """リスト読み込み"""
    
    # カラム、データの確認
    dt = DataTable(data="AAA")
    assert dt.columns == ('0', )
    assert dt.column_count == 1

    rows = dt.rows(type='list')
    assert dt.row_count == 1
    assert rows == [["AAA"],]


    now_dt = datetime.now()
    dt = DataTable(data=now_dt)
    rows = dt.rows(type='list')
    assert dt.columns == ('0', )
    assert dt.column_count == 1

    rows = dt.rows(type='list')
    assert dt.row_count == 1
    assert rows == [[now_dt],]


