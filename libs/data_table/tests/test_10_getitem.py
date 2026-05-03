import pytest
from data_table import DataTable
from pprint import pprint

COLUMNS = ("id", "name", "sex", "age")
RECORDS = [
    [1, "Alice", "F"],
    [2, "Bob", None, 22],
    [3, "Charlie", "M", None],
]

def test_getitem():

    # カラム名の指定なし
    dt = DataTable(data=RECORDS)
    assert dt.columns == ("0", "1", "2", "3")
    assert dt.column_count == 4
    assert dt.row_count    == 3
    assert dt["0"] == [1, 2, 3, ]
    assert dt["3"] == [None, 22, None, ]
    assert dt[-1] == None   # 非存在
    assert dt[100] == None  # 非存在

    # カラム名あり
    dt = DataTable(data=RECORDS, columns=COLUMNS)
    assert dt.columns == COLUMNS
    assert dt.column_count == 4
    assert dt.row_count    == 3
    assert dt["id"] == [1, 2, 3, ]
    assert dt["age"] == [None, 22, None, ]
    assert dt[-1] == None   # 非存在
    assert dt[100] == None  # 非存在
    assert dt["0"] == None  # 非存在




