import pytest
from data_table import DataTable
from pprint import pprint
from datetime import datetime


TABLE_DATA = {
    "id"  : [1       ,  2    , 3        , ],
    "name": ["Alice" , "Bob" , "Charlie", ],
    "sex" : ["F"     , None  , "M"      , ],
    "age" : [None    , 22    ,            ],  # データの不足は None で埋められる
}



def test_column_set():
    """列指向データの読み込み"""


    # 初期状態
    dt = DataTable(data=TABLE_DATA)
    assert dt.column_count == 4
    assert dt.columns == ("id", "name", "sex", "age")


    # 変更
    dt.columns = ["A", "B", "C", "D"]
    assert dt.column_count == 4
    assert dt.columns == ("A", "B", "C", "D")


    # 変更（None は連番に）
    dt.columns = None
    assert dt.column_count == 4
    assert dt.columns == ("0", "1", "2", "3")

    # 文字列に変換
    dt.columns = [0, 11, 22, 33]
    assert dt.column_count == 4
    assert dt.columns == ("0", "11", "22", "33")



def test_length_check():
    """長さチェック"""

    # 初期状態
    dt = DataTable(data=TABLE_DATA)
    assert dt.column_count == 4
    assert dt.columns == ("id", "name", "sex", "age")

    # 長さがアンマッチ（長すぎ）
    with pytest.raises(Exception) as e:
        dt.columns =  ["A", "B", "C", "D", "E"]
    assert e.type == ValueError
    assert e.value.args[0] == "The `column` length does not match the data-length."

    # 長さがアンマッチ（短すぎ）
    with pytest.raises(Exception) as e:
        dt.columns =  ["A", "B", "C"]
    assert e.type == ValueError
    assert e.value.args[0] == "The `column` length does not match the data-length."



def test_length_check_empty_table():
    """長さチェック:レコード0件時は許容"""

    # 初期状態
    dt = DataTable(data={"id": [], "name": [], "sex": [], "age": []})
    assert dt.column_count == 4
    assert dt.columns == ("id", "name", "sex", "age")
    assert dt.row_count == 0

    # 長さがアンマッチ（長すぎ） -> セット可能
    dt.columns =  ["A", "B", "C", "D", "E"]
    assert dt.columns ==  tuple(["A", "B", "C", "D", "E"])
    assert dt.column_count == 5



    # 長さがアンマッチ（短すぎ） -> セット可能
    dt.columns =  ["A", "B", "C"]
    assert dt.columns ==  tuple(["A", "B", "C"])
    assert dt.column_count == 3


    # 長さがアンマッチ（ゼロ） -> セット可能
    dt.columns =  []
    assert dt.columns ==  tuple([])
    assert dt.column_count == 0

    # 長さがアンマッチ（None） -> セット可能
    dt.columns =  None
    assert dt.columns ==  tuple([])
    assert dt.column_count == 0


