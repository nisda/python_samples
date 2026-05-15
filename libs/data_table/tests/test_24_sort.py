import pytest
from data_table import DataTable
from pprint import pprint



def test_sort():
    """ソート"""

    data = [
        {"id": 1, "name": "Alice", "sex": "F"},
        {"id": 2, "sex": None, "name": "Bob", "age": 22},
        {"name": "Charlie", "id": 3, "sex": "M", "age": None},
    ]
    dt = DataTable(data=data)

    # カラム、データの確認
    rows = list(dt.rows(type='dict'))
    assert dt.columns == ("id", "name", "sex", "age")
    assert len(rows) == len(data)

    # sex でソート
    dt = dt.sort(sort_by=["sex"])
    rows = list(dt.rows(type='dict'))
    assert dt.columns == ("id", "name", "sex", "age")
    assert len(rows) == len(data)
    assert rows[0]["id"] == 2
    assert rows[1]["id"] == 1
    assert rows[2]["id"] == 3

    # age, sex でソート
    dt = dt.sort(sort_by=["age", "sex"])
    rows = list(dt.rows(type='dict'))
    assert dt.columns == ("id", "name", "sex", "age")
    assert len(rows) == len(data)
    assert rows[0]["id"] == 3
    assert rows[1]["id"] == 1
    assert rows[2]["id"] == 2




def test_sort_reverse():
    """"逆順ソート"""

    data = [
        {"id": 1, "name": "Alice", "sex": "F",  "age": 18},
        {"id": 2, "name": "Bob"  , "sex": "M",  "age": 20},
        {"id": 3, "name": "Cris" , "sex": None, "age": 18},
    ]
    dt = DataTable(data=data)

    # age, sex で逆順ソート
    dt = dt.sort(sort_by=["age", "sex"], reverse=True)
    rows = list(dt.rows(type='dict'))
    assert dt.columns == ("id", "name", "sex", "age")
    assert len(rows) == len(data)
    assert rows[0]["id"] == 2
    assert rows[1]["id"] == 1
    assert rows[2]["id"] == 3



